from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin
from apps.words.validators import validate_eng_char


class EnglishWord(OwnerMixin):
    word = models.CharField(_('Word'),
                            max_length=100,
                            validators=[validate_eng_char])
    meaning = models.TextField(_('Meaning'), max_length=1000, blank=True)
    readings = models.ManyToManyField('words.Reading',
                                      verbose_name=_('Reading'),
                                      blank=True)
    tags = models.ManyToManyField('words.SearchTag',
                                  verbose_name=_('Search Tags'),
                                  blank=True)
    created_at = models.DateTimeField(_('Created Date'),
                                      auto_now_add=True,
                                      db_index=True)

    class Meta:
        verbose_name = _('English Word')
        unique_together = ('owner', 'word')

    def __str__(self):
        return self.word

    def is_complete(self):
        return self.meaning and self.readings.exists()

    def clean(self):
        if not self.id and EnglishWord.objects.filter(
                word=self.word, owner=self.owner).exists():
            raise ValidationError(
                ugettext("This word already exists in your collection."))

    def save(self, *args, **kwargs):
        if self.word:
            self.word = self.word.lower()
        super(EnglishWord, self).save(*args, **kwargs)
