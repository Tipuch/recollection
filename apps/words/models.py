import logging
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .validators import validate_jap_char, validate_eng_char, validate_hiragana_char, validate_katakana_char
from .managers import JapaneseSyllableManager
from .exceptions import SyllableNotFoundError

logger = logging.getLogger(__name__)


class EnglishWord(models.Model):
    word = models.CharField(_('Word'), max_length=100, validators=[validate_eng_char])
    meaning = models.TextField(_('Meaning'), max_length=500, blank=True)
    readings = models.ManyToManyField('words.Reading', verbose_name=_('Reading'),
                                      related_name='english_words_readings', blank=True)
    created_at = models.DateTimeField(_('Created Date'), auto_now_add=True,
                                      db_index=True)

    class Meta:
        verbose_name = _('English Word')

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        if self.word:
            self.word = self.word.lower()
        super(EnglishWord, self).save(*args, **kwargs)


class JapaneseWord(models.Model):
    word = models.CharField(_('Word'), max_length=100, validators=[validate_jap_char])
    meaning = models.TextField(_('Meaning'), max_length=500, blank=True)
    readings = models.ManyToManyField('words.Reading', verbose_name=_('Readings'),
                                      related_name='words_reading', blank=True)
    kanjis = models.ManyToManyField('words.Kanji', verbose_name=_('Kanjis'),
                                    related_name='words', blank=True)
    created_at = models.DateTimeField(_('Created Date'), auto_now_add=True,
                                      db_index=True)

    class Meta:
        verbose_name = _('Japanese Word')

    def __str__(self):
        return self.word


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

    romaji = models.CharField(_('Romaji Reading'), max_length=100, blank=True, validators=[validate_eng_char])
    hiragana = models.CharField(_('Hiragana Reading'), max_length=50, blank=True, validators=[validate_hiragana_char])
    katakana = models.CharField(_('Katakana Reading'), max_length=50, blank=True, validators=[validate_katakana_char])
    default_display = models.IntegerField(_('Default Display'), choices=CHOICES,
                                          default=settings.READINGS_DEFAULT_DISPLAY)

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
        try:
            # need to check which one has changed from db
            if self.romaji:
                syllables = self.convert_from_romaji()
            elif self.hiragana:
                syllables = self.convert_from_hiragana()
            elif self.katakana:
                syllables = self.convert_from_katakana()
        except SyllableNotFoundError as e:
            logger.warning(e)
        else:
            self.hiragana = ""
            self.katakana = ""
            self.romaji = ""
            self.replace_double_vowels(syllables)
            for syllable in syllables:
                print(syllable)
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

    # need to fix double consonants
    def convert_from_hiragana(self):
        syllables = []
        lookup_method = JapaneseSyllable.objects.lookup_hiragana
        step = 2
        i = 0
        while i < len(self.hiragana):
            # check for double vowels or consonants on next char
            if self.hiragana[i] == self.JP_LONG_VOWEL or self.hiragana[i] in self.DOUBLE_CONSONANTS:
                syllable = JapaneseSyllable.objects.lookup_syllable(JapaneseSyllable.objects.lookup_romaji, syllables[-1].romaji[-1])
            else:
                # look for syllables in next substring (step chars or less)
                next_substring = self.hiragana[i:i+step] if i + step <= len(self.hiragana) - 1 else self.hiragana[i:]
                syllable = JapaneseSyllable.objects.lookup_syllable(lookup_method, next_substring)
            if not syllable:
                raise SyllableNotFoundError("Syllable not found in '{0}'".format(next_substring))
            else:
                syllables.append(syllable)
            i += len(syllable.hiragana)
        print(syllables)
        return syllables

    # need to fix double consonants
    def convert_from_katakana(self):
        syllables = []
        lookup_method = JapaneseSyllable.objects.lookup_katakana
        step = 2
        i = 0
        while i < len(self.katakana):
            # check for double vowels or consonants on next char
            if self.hiragana[i] == self.JP_LONG_VOWEL or self.hiragana[i] in self.DOUBLE_CONSONANTS:
                syllable = JapaneseSyllable.objects.lookup_syllable(JapaneseSyllable.objects.lookup_romaji, syllables[-1].romaji[-1])
            else:
                # look for syllables in next substring (step chars or less)
                next_substring = self.katakana[i:i+step] if i + step <= len(self.katakana) - 1 else self.katakana[i:]
                syllable = JapaneseSyllable.objects.lookup_syllable(lookup_method, next_substring)
            if not syllable:
                raise SyllableNotFoundError("Syllable not found in '{0}'".format(next_substring))
            else:
                syllables.append(syllable)
            i += len(syllable.katakana)
        return syllables

    def replace_double_vowels(self, syllables):
        for index, current in enumerate(syllables):
            if index > 0:
                previous = syllables[index - 1]
                if current.romaji in self.VOWELS and previous.romaji[len(previous.romaji)-1] == current.romaji:
                    current.hiragana = self.JP_LONG_VOWEL
                    current.katakana = self.JP_LONG_VOWEL


class JapaneseSyllable(models.Model):
    romaji = models.CharField(_('Romaji'), max_length=3, validators=[validate_eng_char], db_index=True, unique=True)
    hiragana = models.CharField(_('Hiragana'), max_length=2, validators=[validate_hiragana_char], db_index=True)
    katakana = models.CharField(_('Katakana'), max_length=2, validators=[validate_katakana_char], db_index=True)
    objects = JapaneseSyllableManager()

    def __str__(self):
        return self.romaji
