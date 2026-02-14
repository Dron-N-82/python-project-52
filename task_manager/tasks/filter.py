import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from ..labels.models import Label
from ..statuses.models import Status
from .models import Task, User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        )
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_superuser=0),
        widget=forms.Select(attrs={'class': 'form-control'}),
        )
    self_tasks = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(),
        label=_('Only self tasks'),
        method='filter_self_tasks')

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset