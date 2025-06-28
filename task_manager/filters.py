import django_filters
from django import forms
from .models import Task, Status, Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    labels = django_filters.ModelMultipleChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Labels'),
        widget=forms.CheckboxSelectMultiple,
    )
    
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Only my tasks'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = []