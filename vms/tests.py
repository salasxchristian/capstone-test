from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import VMSCheckIn, VMSOrganization, VMSKioskLocation
from django.test import TestCase
from django.urls import reverse

class VMSCheckInCreateTest(TestCase):
    def setUp(self):
        """Set up necessary objects and user for the test."""
        # Create the test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

        # Fetch the permission for adding a VMSCheckIn and assign it to the test user
        content_type = ContentType.objects.get_for_model(VMSCheckIn)
        add_checkin_perm = Permission.objects.get(
            codename='add_vmscheckin',
            content_type=content_type,
        )
        self.user.user_permissions.add(add_checkin_perm)

        # Fetch the permission for adding a VMSKioskLocation and assign it to the test user
        content_type = ContentType.objects.get_for_model(VMSKioskLocation)
        add_kiosklocation_perm = Permission.objects.get(
            codename='add_vmskiosklocation',
            content_type=content_type,
        )
        self.user.user_permissions.add(add_kiosklocation_perm)

        # Fetch the permission for adding a VMSOrganization and assign it to the test user
        content_type = ContentType.objects.get_for_model(VMSOrganization)
        add_organization_perm = Permission.objects.get(
            codename='add_vmsorganization',
            content_type=content_type,
        )
        self.user.user_permissions.add(add_organization_perm)

        # Save the user with the new permissions
        self.user.save()

        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        # Create a VMSOrganization and VMSKioskLocation for the test
        self.organization = VMSOrganization.objects.create(name='Test Organization')
        self.location = VMSKioskLocation.objects.create(name='Main Entrance')

    def test_create_checkin(self):
        """Test that a logged-in user can check in a guest."""
        data = {
            'full_name': 'Test Guest',
            'reason': 'Meeting',
            'organization': self.organization.pk,
            'location': self.location.pk, 
        }
        response = self.client.post(reverse('vms:checkin'), data)

        # Verify a check-in has been added
        self.assertTrue(VMSCheckIn.objects.filter(full_name='Test Guest').exists(), "Check-in was not successfully created.")