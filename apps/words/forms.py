from django import forms

from .models import JapaneseWord, EnglishWord


class SimplestJpWordForm(forms.ModelForm):
    class Meta:
        model = JapaneseWord
        fields = 'word',


class SimplestEnWordForm(forms.ModelForm):
    class Meta:
        model = EnglishWord
        fields = 'word',
