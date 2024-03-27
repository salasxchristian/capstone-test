from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    # Title of the blog post. Must not exceed 200 characters.
    title = models.CharField(max_length=200)

    # Main content of the blog post. Can be left blank.
    content = models.TextField(null=True, blank=True)

    # Timestamp when the post was added. Automatically set to now when the object is first created.
    date_added = models.DateTimeField(auto_now_add=True)

    # Reference to the User who created the blog post. If the user is deleted, this field is set to null.
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='blog_post_created_by'
    )

    # Timestamp of the last modification. Automatically updated to now every time the object is saved.
    last_modified = models.DateTimeField(auto_now=True)

    # Reference to the User who last modified the blog post. If the user is deleted, this field is set to null.
    last_modified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='blog_post_last_modified_by'
    )

    def __str__(self):
        # String representation of the BlogPost, showing its title.
        return self.title
    
    class Meta:
        # Custom name for the plural form in the admin site.
        verbose_name_plural = "Blog Posts"
