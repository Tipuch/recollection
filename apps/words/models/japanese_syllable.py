from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.managers import JapaneseSyllableManager
from apps.words.validators import validate_eng_char, validate_hiragana_char, validate_katakana_char


class JapaneseSyllable(models.Model):
    romaji = models.CharField(_('Romaji'),
                              max_length=3,
                              db_index=True,
                              unique=True,
                              validators=[validate_eng_char])
    hiragana = models.CharField(
        _('Hiragana'),
        max_length=2,
        db_index=True,
        validators=[validate_hiragana_char],
    )
    katakana = models.CharField(_('Katakana'),
                                max_length=2,
                                db_index=True,
                                validators=[validate_katakana_char])
    objects = JapaneseSyllableManager()

    def __str__(self):
        return self.romaji
