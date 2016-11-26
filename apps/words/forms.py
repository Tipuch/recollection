from django import forms

from .models import EnglishWord, JapaneseWord, Kanji


class SimplestJpWordForm(forms.ModelForm):

    class Meta:
        model = JapaneseWord
        fields = 'word', 'kanjis'

    def _save_m2m(self):
        word = self.cleaned_data['word']
        self.cleaned_data['kanjis'] = Kanji.objects.get_kanjis(word)
        super(SimplestJpWordForm, self)._save_m2m()


class SimplestEnWordForm(forms.ModelForm):

    class Meta:
        model = EnglishWord
        fields = 'word',


class JpWordForm(forms.ModelForm):

    class Meta:
        model = JapaneseWord
        fields = 'word', 'kanjis'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(JpWordForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(JpWordForm, self).save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance

    def _save_m2m(self):
        word = self.cleaned_data['word']
        self.cleaned_data['kanjis'] = Kanji.objects.get_kanjis(word)
        super(SimplestJpWordForm, self)._save_m2m()
