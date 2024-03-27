from django import forms
from .models import *

class VMSCheckInForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=VMSOrganization.objects.all(), 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Organization"
    )
    location = forms.ModelChoiceField(
        queryset=VMSKioskLocation.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select Location"
    )

    class Meta:
        model = VMSCheckIn
        fields = ['full_name', 'reason', 'location', 'organization']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g John Doe'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g Meeting with Jane Doe', 'style': 'height: 100px;'}),
        }

class VMSOrganizationForm(forms.ModelForm):
    class Meta:
        model = VMSOrganization
        fields = ['name', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class VMSKioskLocationForm(forms.ModelForm):
    class Meta:
        model = VMSKioskLocation
        fields = ['name', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g Main Lobby'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }

class VMSKioskTokenForm(forms.ModelForm):
    class Meta:
        model = VMSKioskToken
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g Main Lobby Kiosk'}),
        }

    location = forms.ModelChoiceField(queryset=VMSKioskLocation.objects.all(), empty_label="Select Location", widget=forms.Select(attrs={'class': 'form-select'}))