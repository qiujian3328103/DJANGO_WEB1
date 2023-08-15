from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.bootstrap import Accordion, AccordionGroup
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from .models import FormData

# https://github.com/django-crispy-forms/crispy-bootstrap5
# 
# use the Django Crsipy form bootstrap 5 w
# 

class FormDataForm(forms.ModelForm):
    class Meta:
        model = FormData
        fields = ['username', 'email', 'hyperlink', 'text_area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup(
                    "group name",
                    Row(
                        Column('username', css_class='form-group col-md-6 mb-0'),
                        Column('email', css_class='form-group col-md-6 mb-0'),
                        css_class='form-group row mt-4'
                    ),
                    Row(Column('hyperlink')),
                    Row(Column('text_area')),
                ),
                AccordionGroup(
                    "group name 2",
                    Row(
                        Column(Submit('submit', 'Submit'), css_class='mt-2'),
                        Column(Submit('cancel', 'Cancel', css_class='btn-secondary mt-2')),
                        css_class='form-group row mt-4'
                    ),
                ),
                flush=True,
                always_open=True
            ),
        )