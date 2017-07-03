from django.forms import ModelForm

from core.models import AddOn, AddOnPage


class AddOnForm(ModelForm):
    class Meta:
        model = AddOn
        fields = ['name', 'logo', 'short_description']


class AddOnPageForm(ModelForm):
    class Meta:
        model = AddOnPage
        fields = ['long_description']