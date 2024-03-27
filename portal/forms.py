from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.password_validation import validate_password
from constance import config

class CustomConfigForm(forms.Form):
    APP_NAME = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    LANDING_JB_TITLE = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    LANDING_JB_CONTENT = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    LANDING_JB_LINK = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

    CONFIG = ['APP_NAME', 'LANDING_JB_TITLE', 'LANDING_JB_CONTENT', 'LANDING_JB_LINK']


    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial.update({key: getattr(config, key) for key in self.CONFIG})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def save(self):
        for key in self.CONFIG:
            setattr(config, key, self.cleaned_data[key])