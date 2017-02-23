from django import forms

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
