from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from resources.models import ResourceLinkCategory, ResourceLink
from django.core.exceptions import ValidationError

class ResourceLinkCreateTest(TestCase):
    def setUp(self):
        """Set up the user, permissions, and category for the test."""
        # Create the test user and log in
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        # Grant the test user permission to add a resource link
        add_link_perm = Permission.objects.get(codename='add_resourcelink')
        self.user.user_permissions.add(add_link_perm)
        self.user.save()
        self.client.login(username=self.username, password=self.password)
        # Create a test category for the resource link
        self.category = ResourceLinkCategory.objects.create(name='Test Category', last_modified_by=self.user)

    def test_create_link(self):
        """Test that a user with permission can create a resource link."""
        data = {
            'title': 'Test Link', 
            'url': 'https://www.example.com/', 
            'category': self.category.id,
            'is_internal': False,
        }
        # Get the initial count of resource links
        initial_link_count = ResourceLink.objects.count()

        response = self.client.post(reverse('resources:create_link'), data)
        
        # Verify the link count has increased by one
        self.assertEqual(ResourceLink.objects.count(), initial_link_count + 1, "Resource link count did not increase after creation.")
        
        # Ensure the new link exists and has the correct attributes
        new_link = ResourceLink.objects.get(title='Test Link')
        self.assertEqual(new_link.url, 'https://www.example.com/', "New link URL does not match the expected value.")
        self.assertEqual(new_link.category.id, self.category.id, "New link category does not match the expected value.")
