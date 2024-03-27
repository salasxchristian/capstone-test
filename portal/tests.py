from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class LandingPageTest(TestCase):
    def setUp(self):
        """Set up the user for the test."""
        # Create the test user and log in
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

    def test_landing_page_accessible(self):
        """Test that the landing page is accessible to logged-in users and contains expected content."""

        # Get the response
        response = self.client.get(reverse('portal:landing'))
        
        # Check that the response status code is 200 and OK
        self.assertEqual(response.status_code, 200, f"Expected status code 200, got {response.status_code}")

        # Check if the response context has a user and the user is authenticated
        self.assertTrue(response.context['user'].is_authenticated, "User should be authenticated")

        # Check that the jumbotron on the landing page contains the expected text
        expected_content = 'Welcome'
        self.assertContains(response, expected_content, status_code=200, msg_prefix="Landing page doesn't contain expected text.")
