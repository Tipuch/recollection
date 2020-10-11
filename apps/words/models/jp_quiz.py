from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin


class JPQuiz(OwnerMixin):
    quiz_template = models.ForeignKey('words.JPQuizTemplate',
                                      verbose_name=_('Quiz Template'),
                                      on_delete=models.CASCADE)
    completed_at = models.DateTimeField(_('Completed At'),
                                        blank=True,
                                        null=True)
    question_index = models.PositiveIntegerField(_('Question Index'),
                                                 default=0)
