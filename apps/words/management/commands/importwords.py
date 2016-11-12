from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.words.forms import SimplestEnWordForm, SimplestJpWordForm
from apps.words.models import JapaneseWord


class Command(BaseCommand):
    help = 'Loads words from file into the site'

    def add_arguments(self, parser):
        parser.add_argument('-o', dest='owner', type=str,
                            help=('The user who will'
                                  ' be the owner of the words added'))
        parser.add_argument(dest='filepath', type=str,
                            help=('the filepath to the text'
                                  ' file containing the words'))
        parser.add_argument('-jp', dest='jp', action='store_true',
                            help='use this if you have japanese words')
        parser.add_argument('-en', dest='en', action='store_true',
                            help='use this if you have english words')

    def handle(self, *args, **kwargs):
        if not kwargs.get('jp') and not kwargs.get('en'):
            raise CommandError('You need to specify either -jp or -en.')
        if kwargs.get('jp') and kwargs.get('en'):
            raise CommandError('You can\'t have both -jp and -en')
        if not kwargs.get('owner'):
            raise CommandError('You need to specify the owner of the words')
        owner = get_user_model().objects.get(username=kwargs.get('owner'))
        words = [word.rstrip('\n') for word in open(kwargs.get('filepath'))]
        lang = 'jp' if kwargs.get('jp') else 'en'
        self.process_words(words, lang, owner)

    def process_words(self, words, lang, owner):
        choices = {
            'jp': {
                'form_class': SimplestJpWordForm,
                'verbose': 'Japanese'
            },
            'en': {
                'form_class': SimplestEnWordForm,
                'verbose': 'English'
            }
        }
        for word in words:
            form = choices[lang]['form_class'](data={'word': word})
            if form.is_valid():
                valid_word = form.save(commit=False)
                valid_word.owner = owner
                valid_word.save()
                form.save_m2m()
            else:
                self.stderr.write(
                    '{word}, is not a valid {language} word.'.format(
                        **{'word': word, 'language': choices[lang]['verbose']}
                        ))
