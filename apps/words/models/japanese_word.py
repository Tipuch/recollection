from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin
from apps.words.validators import validate_jap_char


class JapaneseWord(OwnerMixin):
    word = models.CharField(_('Word'),
                            max_length=100,
                            validators=[validate_jap_char])
    meaning = models.TextField(_('Meaning'), max_length=1000, blank=True)
    readings = models.ManyToManyField('words.Reading',
                                      verbose_name=_('Readings'),
                                      blank=True)
    kanjis = models.ManyToManyField('words.Kanji',
                                    verbose_name=_('Kanjis'),
                                    blank=True)
    tags = models.ManyToManyField('words.SearchTag',
                                  verbose_name=_('Search Tags'),
                                  blank=True)
    created_at = models.DateTimeField(_('Created Date'),
                                      auto_now_add=True,
                                      db_index=True)

    class Meta:
        verbose_name = _('Japanese Word')
        unique_together = ('owner', 'word')

    def __str__(self):
        return self.word

    def clean(self):
        if not self.id and JapaneseWord.objects.filter(
                word=self.word, owner=self.owner).exists():
            raise ValidationError(
                ugettext(
                    "The word [%(word)s] already exists in your collection.") %
                {'word': self.word})

    def is_complete(self):
        return self.meaning and self.readings.exists()
