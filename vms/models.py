from django.db import models
from django.core.exceptions import ValidationError
import uuid

class VMSOrganization(models.Model):
    name = models.CharField(max_length=250, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.check_ins.exists():
            raise ValidationError(f'Cannot delete Organization <u>{self.name}</u> because it is associated with one or more visitor check-ins.')
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Organizations"

class VMSKioskLocation(models.Model):
    name = models.CharField(max_length=250, unique=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        if self.tokens.exists() or self.check_ins.exists():
            raise ValidationError(f"Cannot delete Kiosk Location <u>{self.name}</u> because it is associated with one or more Kiosk Links or visitor check-ins.")
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Kiosk Locations"

class VMSCheckIn(models.Model):
    full_name = models.CharField(max_length=200)
    checkin_date = models.DateTimeField(auto_now_add=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey(VMSOrganization, on_delete=models.PROTECT, null=True, blank=True, related_name='check_ins')
    reason = models.TextField(blank=True)
    location = models.ForeignKey(VMSKioskLocation, on_delete=models.PROTECT, null=True, blank=True, related_name='check_ins')

    def __str__(self):
        return f"{self.full_name} - {self.checkin_date}"
    
    class Meta:
        verbose_name_plural = "Check Ins"

class VMSKioskToken(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.ForeignKey('VMSKioskLocation', on_delete=models.PROTECT, related_name='tokens')
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Token {self.token}"

