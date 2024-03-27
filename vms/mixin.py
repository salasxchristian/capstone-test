from .models import VMSKioskToken
from django.core.exceptions import PermissionDenied

class TokenRequiredMixin:
    """Mixin to require a valid token for accessing a view."""
    def dispatch(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            try:
                kiosk_token = VMSKioskToken.objects.get(token=token)
            except VMSKioskToken.DoesNotExist:
                raise PermissionDenied("Token does not exist.")
        else:
            raise PermissionDenied("No token provided.")
        
        return super().dispatch(request, *args, **kwargs)