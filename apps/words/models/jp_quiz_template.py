import random

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.words.modelmixins import OwnerMixin
from . import JPQuizQuestion, JPQuiz


class JPQuizTemplate(OwnerMixin):
    CHOICES_NUMBER = 6

    words = models.ManyToManyField('words.JapaneseWord',
                                   verbose_name=_('Words'))
    title = models.CharField(_('Title'), max_length=100, unique=True)
    # frequency in days
    frequency = models.PositiveIntegerField(_('Frequency in days'), default=7)
    number_of_questions = models.PositiveIntegerField(_('Number of questions'),
                                                      default=20)

    def create_quiz(self):
        quiz = JPQuiz.objects.create(quiz_template=self, owner=self.owner)
        # get random subset of words
        answer_words = self.words.order_by('?')[:self.number_of_questions]
        questions = []
        words = list(self.words)
        for i, answer_word in enumerate(answer_words):
            choices = {answer_word}

            while len(choices) < self.CHOICES_NUMBER:
                choice = random.choice(words)
                if choice == answer_word:
                    continue
                else:
                    choices.add(choice)

            questions.append(
                JPQuizQuestion(quiz=quiz,
                               choices=list(choices),
                               right_answer=answer_word,
                               index=i,
                               owner=self.owner))
        JPQuizQuestion.objects.bulk_create(questions)
