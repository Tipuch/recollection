from django.forms import BaseFormSet

from .forms import JpWordForm


class JpWordFormset(BaseFormSet):
    """
    This formset will probably contain the media (css, js)
    necessary for being dynamic
    """
