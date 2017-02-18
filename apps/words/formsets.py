from django.forms import BaseFormSet
from django.utils.translation import ugettext

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class BaseJpWordFormset(BaseFormSet):
    """
    This formset will probably contain the media (css, js)
    necessary for being dynamic
    """


class BaseJpWordFormsetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(BaseJpWordFormsetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_id = "id-JpWordFormset"
        self.render_required_fields = True
        self.add_input(Button("add", ugettext("Add")))
        self.add_input(Button("delete", ugettext("Delete")))
        self.add_input(Submit("submit", ugettext("Save")))
