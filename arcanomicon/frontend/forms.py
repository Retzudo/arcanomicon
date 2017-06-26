from django.forms import ModelForm
from django import forms

from core.models import AddOn


class AddOnForm(ModelForm):
    long_description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = AddOn
        fields = ['name', 'logo', 'short_description']