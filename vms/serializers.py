from rest_framework import serializers
from .models import VMSKioskToken

class VMSKioskTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VMSKioskToken
        fields = ['id', 'name', 'location', 'token', 'created_at']
