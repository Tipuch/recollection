from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .validators import validate_jap_char, validate_eng_char, validate_hiragana_char, validate_katakana_char


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
    CHOICES = (
        (1, _('Romaji')),
        (2, _('Hiragana')),
        (3, _('Katakana')),
    )

    romaji = models.CharField(_('Romaji Reading'), max_length=100, blank=True, validators=[validate_eng_char])
    hiragana = models.CharField(_('Hiragana Reading'), max_length=50, blank=True, validators=[validate_hiragana_char])
    katakana = models.CharField(_('Katakana Reading'), max_length=50, blank=True, validators=[validate_katakana_char])
    default_display = models.IntegerField(_('Default Display'), choices=CHOICES,
                                          default=settings.READINGS_DEFAULT_DISPLAY)

    def __str__(self):
        choices = {
            1: self.romaji,
            2: self.hiragana,
            3: self.katakana
        }
        return choices.get(self.default_display) or '???'

    def save(self, *args, **kwargs):
        if self.romaji:
            self.romaji = self.romaji.lower()
        super(Reading, self).save(*args, **kwargs)
