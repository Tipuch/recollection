from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.words.word_parser import process_file


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
        lang = 'jp' if kwargs.get('jp') else 'en'
        try:
            process_file(kwargs.get('filepath'), lang, owner)
        except ValueError as e:
            self.stderr.write(e)
