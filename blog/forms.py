from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My Blog Post Title'}),
            'content': SummernoteWidget(),
        }