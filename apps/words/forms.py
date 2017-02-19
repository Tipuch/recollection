from django import forms
from django.utils.translation import ugettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import EnglishWord, JapaneseWord, Kanji


class SimplestJpWordForm(forms.ModelForm):

    class Meta:
        model = JapaneseWord
        fields = 'word', 'kanjis'
        widgets = {
            'kanjis': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(SimplestJpWordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-simplestJpWordForm"
        self.helper.form_method = "post"
        self.helper.add_input(Submit('submit', ugettext("Save")))

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
        self.cleaned_data['kanjis'] = Kanji.objects.get_kanjis(word)
        super(JpWordForm, self)._save_m2m()
