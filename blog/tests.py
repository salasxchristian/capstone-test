from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import BlogPost

class BlogPostCreateTest(TestCase):
    def setUp(self):
        """Set up the user and permissions for the test."""
        # Create the test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        # Assign the test user permissions to add a blog post and log in
        add_blogpost_perm = Permission.objects.get(codename='add_blogpost')
        self.user.user_permissions.add(add_blogpost_perm)
        self.user.save()
        self.client.login(username=self.username, password=self.password)

    def test_create_post(self):
        """Test that a user with permission can create a blog post."""
        data = {'title': 'Test Post', 'content': 'This is a test post.'}
        initial_post_count = BlogPost.objects.count()
        
        # Attempt to create a new blog post
        response = self.client.post(reverse('blog:create_post'), data)

        # Verify the post count has increased by one
        self.assertEqual(BlogPost.objects.count(), initial_post_count + 1, "Blog post count did not increase after creation.")
        
        # Ensure the new blog post exists and matches the submitted data
        post_exists = BlogPost.objects.filter(title='Test Post', content='This is a test post.').exists()
        self.assertTrue(post_exists, "Created blog post does not exist or doesn't match the submitted data.")
