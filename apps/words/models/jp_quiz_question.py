from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin


class JPQuizQuestion(OwnerMixin):
    quiz = models.ForeignKey('words.JPQuiz',
                             verbose_name=_('Quiz'),
                             on_delete=models.CASCADE)
    choices = models.ManyToManyField('words.JapaneseWord',
                                     verbose_name=_('Choices'),
                                     related_name='questions_as_choices')
    right_answer = models.ForeignKey('words.JapaneseWord',
                                     verbose_name=_('Right answer'),
                                     related_name='questions_as_answer',
                                     on_delete=models.CASCADE)
    index = models.PositiveIntegerField(_('Index'))
