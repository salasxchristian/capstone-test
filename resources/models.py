from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

class ResourceLinkCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, error_messages={'unique': 'A Link Category with that name already exists. Please enter a unique name.'})
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='link_category_last_modified_by')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.links.exists():
            raise ValidationError('You cannot delete a Link Category if it has links associated with it. Please delete the links first.')
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Resource Link Categories"

class ResourceLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(validators=[URLValidator()])
    description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='last_modified_by')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(ResourceLinkCategory, on_delete=models.PROTECT, related_name='links')
    is_internal = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title    

    class Meta:
        verbose_name_plural = "Resource Links"