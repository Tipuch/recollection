from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin


class JPQuizAnswer(OwnerMixin):
    answer = models.ForeignKey('words.JapaneseWord',
                               verbose_name=_('Answer'),
                               on_delete=models.CASCADE)
    question = models.OneToOneField('words.JPQuizQuestion',
                                    verbose_name=_('Question'),
                                    related_name='answer',
                                    on_delete=models.CASCADE)
    right = models.BooleanField(_('Right Answer'))
