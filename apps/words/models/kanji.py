from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.managers import KanjiManager
from apps.words.modelmixins import OwnerMixin


class Kanji(OwnerMixin):
    character = models.CharField(_('Kanji'), max_length=1)
    meaning = models.TextField(_('Meaning'), max_length=500, blank=True)
    readings = models.ManyToManyField('words.Reading',
                                      verbose_name=_('Readings'),
                                      related_name='kanjis_reading',
                                      blank=True)

    objects = KanjiManager()

    class Meta:
        unique_together = ('owner', 'character')

    def __str__(self):
        return self.character
