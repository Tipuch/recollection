from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin


class JPQuizTemplate(OwnerMixin):
    words = models.ManyToManyField('words.JapaneseWord',
                                   verbose_name=_('Words'))
    title = models.CharField(_('Title'), max_length=100, unique=True)
    # frequency in days
    frequency = models.PositiveIntegerField(_('Frequency in days'), default=7)
    number_of_questions = models.PositiveIntegerField(_('Number of questions'),
                                                      default=20)
