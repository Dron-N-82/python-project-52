from django import forms
from django.core.exceptions import ValidationError
from .models import Label
from django.utils.translation import gettext as _


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': _('Name')}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control',
                    'required': True}),
            }