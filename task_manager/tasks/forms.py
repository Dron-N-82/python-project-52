from django import forms

# from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Label, Status, Task, User


class CreateTaskForm(forms.ModelForm):
    # status = forms.ModelChoiceField(
    #     queryset=Status.objects.all(),
    #     # queryset=Task.objects.values_list('status', flat=True).distinct(),
    #     label=_('Status'),
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    # executor = forms.ModelChoiceField(
    #     # queryset=User.objects.all(),
    #     queryset=User.objects.filter(is_superuser=0),
    #     # queryset=Task.objects.values_list('status', flat=True).distinct(),
    #     label=_('Executor'),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False
    # )
    # label = forms.ModelMultipleChoiceField(
    #     queryset=Label.objects.all(),
    #     # queryset=Task.objects.values_list('label', flat=True).distinct(),
    #     label=_('Labels'),
    #     widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    #     required=False
    # )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']
        # labels = {
        #     'name': _('Name'),
        #     'description': _('Description'),
        #     'status': _('Status')
        #     }
        widgets = {
            # 'name': forms.TextInput(
            #     attrs={'class': 'form-control',
            #         'required': True}),
            # 'description': forms.Textarea(attrs={
            #     'placeholder': _('Description'),
            #     'class': 'form-control',
            #     'rows': 10}),
            'labels': forms.SelectMultiple(
                attrs={'class': 'form-control'}),
            }
        

class ViewTaskForm(forms.ModelForm):
    pass