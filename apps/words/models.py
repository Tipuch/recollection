import logging

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import FieldTracker

from .exceptions import SyllableNotFoundError
from .managers import JapaneseSyllableManager
from .validators import (validate_eng_char, validate_hiragana_char,
                         validate_jap_char, validate_katakana_char)

logger = logging.getLogger(__name__)


class EnglishWord(models.Model):
    word = models.CharField(_('Word'), max_length=100, validators=[validate_eng_char])
    meaning = models.TextField(_('Meaning'), max_length=1000, blank=True)
    readings = models.ManyToManyField('words.Reading', verbose_name=_('Reading'), blank=True)
    tags = models.ManyToManyField('words.SearchTag', verbose_name=_('Search Tags'), blank=True)
    created_at = models.DateTimeField(_('Created Date'), auto_now_add=True, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('English Word')

    def __str__(self):
        return self.word

    def is_owner(self, user):
        return self.owner == user or user.is_superuser

    def is_complete(self):
        return self.meaning and self.readings.count()

    def save(self, *args, **kwargs):
        if self.word:
            self.word = self.word.lower()
        super(EnglishWord, self).save(*args, **kwargs)


class JapaneseWord(models.Model):
    word = models.CharField(_('Word'), max_length=100, validators=[validate_jap_char])
    meaning = models.TextField(_('Meaning'), max_length=1000, blank=True)
    readings = models.ManyToManyField('words.Reading', verbose_name=_('Readings'), blank=True)
    kanjis = models.ManyToManyField('words.Kanji', verbose_name=_('Kanjis'), blank=True)
    tags = models.ManyToManyField('words.SearchTag', verbose_name=_('Search Tags'), blank=True)
    created_at = models.DateTimeField(_('Created Date'), auto_now_add=True, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Owner'))

    class Meta:
        verbose_name = _('Japanese Word')

    def __str__(self):
        return self.word

    def is_owner(self, user):
        return self.owner == user or user.is_superuser

    def is_complete(self):
        return self.meaning and self.readings.count()


class Kanji(models.Model):
    character = models.CharField(_('Kanji'), max_length=1)
    meaning = models.TextField(_('Meaning'), max_length=500, blank=True)
    readings = models.ManyToManyField('words.Reading', verbose_name=_('Readings'),
                                      related_name='kanjis_reading', blank=True)

    def __str__(self):
        return self.character


class Reading(models.Model):
    VOWELS = ('a', 'e', 'i', 'o', 'u', 'y')
    ROMAJI, HIRAGANA, KATAKANA = range(1, 4)
    JP_LONG_VOWEL = '\u30fc'
    DOUBLE_CONSONANTS = '\u3063', '\u30c3'
    CHOICES = (
        (ROMAJI, _('Romaji')),
        (HIRAGANA, _('Hiragana')),
        (KATAKANA, _('Katakana')),
    )

    romaji = models.CharField(_('Romaji Reading'), max_length=100, blank=True, validators=[validate_eng_char], db_index=True)
    hiragana = models.CharField(_('Hiragana Reading'), max_length=50, blank=True, validators=[validate_hiragana_char], db_index=True)
    katakana = models.CharField(_('Katakana Reading'), max_length=50, blank=True, validators=[validate_katakana_char], db_index=True)
    default_display = models.IntegerField(_('Default Display'), choices=CHOICES,
                                          default=settings.READINGS_DEFAULT_DISPLAY)

    field_tracker = FieldTracker()

    def __str__(self):
        choices = {
            self.ROMAJI: self.romaji,
            self.HIRAGANA: self.hiragana,
            self.KATAKANA: self.katakana
        }
        return choices.get(self.default_display) or '???'

    def save(self, *args, **kwargs):
        if self.romaji:
            self.romaji = self.romaji.lower()
        self.convert_reading()
        super(Reading, self).save(*args, **kwargs)

    def convert_reading(self):
        syllables = []
        conversion_flag = False
        try:
            # need to check which one has changed from db
            if self.field_tracker.has_changed('romaji') and self.romaji:
                conversion_flag = True
                syllables = self.convert_from_romaji()
            elif self.field_tracker.has_changed('hiragana') and self.hiragana:
                conversion_flag = True
                syllables = self.convert_from_japanese_character(self.HIRAGANA)
            elif self.field_tracker.has_changed('katakana') and self.katakana:
                conversion_flag = True
                syllables = self.convert_from_japanese_character(self.KATAKANA)
        except SyllableNotFoundError as e:
            logger.warning(e)
        else:
            if conversion_flag:
                self.hiragana = ""
                self.katakana = ""
                self.romaji = ""
                self.replace_double_vowels(syllables)
                for syllable in syllables:
                    self.hiragana += syllable.hiragana
                    self.katakana += syllable.katakana
                    self.romaji += syllable.romaji

    def convert_from_romaji(self):
        syllables = []
        lookup_method = JapaneseSyllable.objects.lookup_romaji
        step = 3
        i = 0
        while i < len(self.romaji):
            # look for syllables in next substring (step chars or less)
            next_substring = self.romaji[i:i+step] if i + step <= len(self.romaji) - 1 else self.romaji[i:]
            syllable = JapaneseSyllable.objects.lookup_syllable(lookup_method, next_substring)
            if not syllable:
                raise SyllableNotFoundError("Syllable not found in '{0}'".format(next_substring))
            else:
                syllables.append(syllable)
            i += len(syllable.romaji)
        return syllables


    def convert_from_japanese_character(self, alphabet_id):
        alphabet_const = {
            self.HIRAGANA: {
                'lookup_method': JapaneseSyllable.objects.lookup_hiragana,
                'attr': 'hiragana'
            },
            self.KATAKANA: {
                'lookup_method': JapaneseSyllable.objects.lookup_katakana,
                'attr': 'katakana'
            }
        }
        syllables = []
        alphabet_props = alphabet_const[alphabet_id]
        self_prop = getattr(self, alphabet_props['attr'])
        step = 2
        i = 0
        while i < len(self_prop):
            # reset double consonants flag
            double_consonants_flag = False
            # check for double vowels or consonants on next char
            if self_prop[i] == self.JP_LONG_VOWEL:
                syllable = JapaneseSyllable.objects.lookup_syllable(JapaneseSyllable.objects.lookup_romaji, syllables[-1].romaji[-1])
            else:
                # look for double consonants character
                if self_prop[i] in self.DOUBLE_CONSONANTS:
                    double_consonants_flag = True
                    i += 1
                # look for syllables in next substring (step chars or less)
                next_substring = self_prop[i:i+step] if i + step <= len(self_prop) - 1 else self_prop[i:]
                syllable = JapaneseSyllable.objects.lookup_syllable(alphabet_props['lookup_method'], next_substring)
            if not syllable:
                raise SyllableNotFoundError("Syllable not found in '{0}'".format(next_substring))
            else:
                if double_consonants_flag:
                    double_consonants_syll = JapaneseSyllable.objects.lookup_syllable(
                        JapaneseSyllable.objects.lookup_romaji, syllable.romaji[0]
                    )
                    syllables.append(double_consonants_syll)
                syllables.append(syllable)
            i += len(getattr(syllable, alphabet_props['attr']))
        return syllables


    def replace_double_vowels(self, syllables):
        for index, current in enumerate(syllables):
            if index > 0:
                previous = syllables[index - 1]
                if current.romaji in self.VOWELS and previous.romaji[len(previous.romaji)-1] == current.romaji:
                    current.katakana = self.JP_LONG_VOWEL


class JapaneseSyllable(models.Model):
    romaji = models.CharField(_('Romaji'), max_length=3, validators=[validate_eng_char], db_index=True, unique=True)
    hiragana = models.CharField(_('Hiragana'), max_length=2, validators=[validate_hiragana_char], db_index=True)
    katakana = models.CharField(_('Katakana'), max_length=2, validators=[validate_katakana_char], db_index=True)
    objects = JapaneseSyllableManager()

    def __str__(self):
        return self.romaji


class SearchTag(models.Model):
    eng_tag = models.CharField(_('English Tag'), max_length=50, validators=[validate_eng_char], db_index=True, blank=True)
    jap_tag = models.CharField(_('Japanese Tag'), max_length=25, validators=[validate_jap_char], db_index=True, blank=True)

    class Meta:
        verbose_name = _('Search Tag')

    def __str__(self):
        return '{0} {1}'.format(self.eng_tag, self.jap_tag)
