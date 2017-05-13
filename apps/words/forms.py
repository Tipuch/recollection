import os
from tempfile import NamedTemporaryFile

from django import forms

from apps.words.word_parser import process_file
from .models import EnglishWord, JapaneseWord, Kanji


class EnWordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(EnWordForm, self).__init__(*args, **kwargs)
        self.fields['owner'].initial = self.user.id

    class Meta:
        model = EnglishWord
        fields = 'word', 'owner'


class JpWordForm(forms.ModelForm):

    class Meta:
        model = JapaneseWord
        fields = 'word', 'kanjis', 'owner'
        widgets = {
            'kanjis': forms.HiddenInput(),
            'owner': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(JpWordForm, self).__init__(*args, **kwargs)
        self.fields['owner'].initial = self.user.id

    def _save_m2m(self):
        word = self.cleaned_data['word']
        self.cleaned_data['kanjis'] = Kanji.objects.get_kanjis(
            word, owner=self.cleaned_data['owner'])
        super(JpWordForm, self)._save_m2m()


class WordsUploadForm(forms.Form):
    words = forms.FileField()

    class Media:
        js = (
            'static/words/js/WordsUploadForm.js',
            'https://cdnjs.cloudflare.com/ajax/libs/notify/0.4.2/notify.min.js')

    def handle_uploaded_file(self, lang, owner):
        if self.is_valid():
            f = self.cleaned_data["words"]
            destination = NamedTemporaryFile(delete=False)
            filepath = destination.name
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            try:
                process_file(filepath, lang, owner)
            except ValueError:
                raise
            finally:
                # always remove temporary file
                os.unlink(filepath)
