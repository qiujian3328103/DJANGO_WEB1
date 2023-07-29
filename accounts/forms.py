from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import FormData

class FormDataForm(forms.ModelForm):
    class Meta:
        model = FormData
        fields = ['username', 'email', 'hyperlink', 'text_area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
            Column('username', css_class='form-group col-md-6 mb-0'),
            Column('email', css_class='form-group col-md-6 mb-0'),
            css_class='for-group row mt-4'
            ),
            Row(Column('hyperlink')),
            Row(Column('text_area')),
            Row(
            Column(Submit('submit', 'Submit'), css_class='mt-4'),
            Column(Submit('cancel', 'Cancel', css_class='btn-secondary; mt-4')),
            css_class='for-group row mt-4'
            ),
        )