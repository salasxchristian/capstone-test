from django import forms
from .models import *

class ResourceLinkForm(forms.ModelForm):
    is_internal = forms.ChoiceField(choices=[('', 'Select a Link Type'), (True, 'Internal'), (False, 'External')], label='Link Type', initial='', widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=ResourceLinkCategory.objects.all(), empty_label="Select a Category", widget=forms.Select(attrs={'class': 'form-select'}))
    class Meta:
        model = ResourceLink
        fields = ['title', 'url', 'description', 'is_internal', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Team Knowledge Base'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g. https://kb.awesometeam.com'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g. A place to store all of our team knowledge.'}),
        }
    
    def __init__(self, *args, **kwargs):
            category_id = kwargs.pop('category_id', None)
            super().__init__(*args, **kwargs)
            if category_id:
                self.fields['category'].initial = category_id

class ResourceLinkCategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceLinkCategory
        fields = ['name']  # replace 'name' with the actual field name in your Category model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Employee Resources'}),
        }