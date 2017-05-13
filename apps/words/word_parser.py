import logging
from .forms import JpWordForm, EnWordForm

logger = logging.getLogger(__name__)


def process_file(filepath, lang, owner):
    words = [word.rstrip('\n') for word in open(filepath)]
    process_words(words, lang, owner)


def process_words(words, lang, owner):
    choices = {
        'jp': {
            'form_class': JpWordForm,
            'verbose': 'Japanese'
        },
        'en': {
            'form_class': EnWordForm,
            'verbose': 'English'
        }
    }
    for word in words:
        form = choices[lang]['form_class'](
            data={'word': word, 'user': owner})
        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
        else:
            error_message = '{word}, is not a valid {language} word.'.format(
                **{'word': word, 'language': choices[lang]['verbose']}
            )
            logger.error(error_message)
            raise ValueError(error_message)
