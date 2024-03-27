import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.views.generic.base import TemplateView
from .mixin import TokenRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from urllib.parse import urlencode
from django.views import View
from rest_framework import generics
from .serializers import VMSKioskTokenSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.utils.dateparse import parse_date
import csv

class VMSCheckInCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = VMSCheckIn
    form_class = VMSCheckInForm
    permission_required = 'vms.add_vmscheckin'
    permission_denied_message = "You do not have permission to check in visitors"
    template_name = 'checkin.html'
    context_object_name = 'checkins'
    success_url = reverse_lazy('vms:checkin_active') 

    def form_valid(self, form):
        messages.success(self.request, f'Guest <u>{form.instance.full_name}</u> has been checked in successfully.')
        return super().form_valid(form)

class VMSKioskCheckInCreateView(TokenRequiredMixin, CreateView):
    model = VMSCheckIn
    form_class = VMSCheckInForm
    template_name = 'checkin.html'

    def get_success_url(self):
        """
        Generate the success URL to redirect to after the form submission.
        This method appends the token query parameter to retain it in the URL.
        """
        token = self.request.GET.get('token')
        if token:
            # Manually append the token parameter
            return f"{reverse('vms:kiosk_checkin')}?token={token}"
        else:
            # Fallback to a default URL if no token is found
            return reverse('vms:kiosk_checkin')

class VMSCheckInHistoryView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    '''
    This view is used to display the Check In history of the vms.
    '''
    model = VMSCheckIn
    permission_required = 'vms.view_vmscheckin'
    permission_denied_message = "You do not have permission to view the check-in history"
    template_name = 'checkin_history.html'
    context_object_name = 'guests'
    paginate_by = 20

    def get_queryset(self):
        '''
        This function handles the filtering of the check-ins based on the search query, start date, and end date.

        By default it returns all the check-ins that are not active and orders them by the checkout date in descending order.

        If a search query is provided, the queryset is filtered to include only the check-ins where the full name, reason, organization name, or location name contains the search query.

        If a start date is provided, the queryset is filtered to include only the check-ins where the check-in date is greater than or equal to the start date.

        If an end date is provided, the queryset is filtered to include only the check-ins where the check-in date is less than or equal to the end date.

        The filtered queryset is then returned.
        '''
        queryset = VMSCheckIn.objects.filter(is_active=False).order_by('-checkout_date')
        search_query = self.request.GET.get('search', '').strip()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(reason__icontains=search_query) |
                Q(organization__name__icontains=search_query) |
                Q(location__name__icontains=search_query)
            )
        
        if start_date:
            start_date = parse_date(start_date)
            queryset = queryset.filter(checkin_date__date__gte=start_date)
        
        if end_date:
            end_date = parse_date(end_date)
            queryset = queryset.filter(checkin_date__date__lte=end_date)
        
        return queryset
    
    def render_to_response(self, context, **response_kwargs):
        if 'export' in self.request.GET:
            return self.export_checkins_as_csv()
        return super().render_to_response(context, **response_kwargs)

    # Export the check-ins as a CSV file
    def export_checkins_as_csv(self):
        '''
        This function exports the visitor history as a CSV file.

        It first sets up the HTTP response with the appropriate headers for a CSV file download. 
        The filename is set to "checkin_history.csv".

        A CSV writer is then created for the response. The first row of the CSV file is written with the column headers.

        The function then iterates over the queryset returned by `self.get_queryset()`. For each check-in, a row is written to the CSV file. 
        Each row contains the full name, check-in date, check-out date, organization, reason, and location of the check-in. 
        If the check-out date, organization, or location is not set, an empty string is written instead.

        Finally, the HTTP response, which now contains the CSV file, is returned.
        '''
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="checkin_history.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Check-in Date', 'Check-out Date', 'Organization', 'Reason', 'Location'])

        for checkin in self.get_queryset():
            writer.writerow([
                checkin.full_name,
                checkin.checkin_date.strftime('%Y-%m-%d %H:%M:%S'),
                checkin.checkout_date.strftime('%Y-%m-%d %H:%M:%S') if checkin.checkout_date else '',
                checkin.organization.name if checkin.organization else '',
                checkin.reason,
                checkin.location.name if checkin.location else '',
            ])

        return response

class ActiveVMSCheckInView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = VMSCheckIn
    permission_required = 'vms.view_vmscheckin'
    permission_denied_message = "You do not have permission to view the active check-ins"
    template_name = 'checkin_active.html'
    context_object_name = 'guests'

    def get_queryset(self):
        return VMSCheckIn.objects.filter(is_active=True).order_by('-checkin_date')
    
class VMSCheckOut(LoginRequiredMixin, PermissionRequiredMixin,  UpdateView):
    model = VMSCheckIn
    fields = []
    permission_required = 'vms.change_vmscheckin'
    permission_denied_message = "You do not have permission to check out visitors"
    template_name = 'checkout.html'
    success_url = reverse_lazy('vms:checkin_history')
    context_object_name = 'guest'

    def form_valid(self, form):
        form.instance.is_active = False
        form.instance.checkout_date = timezone.now()
        messages.success(self.request, f'Guest <u>{form.instance.full_name}</u> has been checked out successfully.')
        return super().form_valid(form)
        
class VMSOrganizationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VMSOrganization
    form_class = VMSOrganizationForm
    template_name = 'kiosk/org_create.html'
    success_url = reverse_lazy('vms:settings')

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

class VMSOrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VMSOrganization
    form_class = VMSOrganizationForm
    template_name = 'kiosk/org_edit.html'
    success_url = reverse_lazy('vms:settings')

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

class VMSOrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VMSOrganization
    template_name = 'kiosk/org_delete.html'
    context_object_name = 'organization'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition
        
    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            try:
                self.object.delete()
                messages.success(request, f'Organization named {self.object.name} has been deleted successfully.')
            except Exception as e:
                messages.error(request, e.args[0])
            return redirect('vms:settings')

class VMSKioskLocationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VMSKioskLocation
    form_class = VMSKioskLocationForm
    template_name = 'kiosk/location_create.html'
    success_url = reverse_lazy('vms:settings')

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

class VMSKioskLocationEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VMSKioskLocation
    form_class = VMSKioskLocationForm
    template_name = 'kiosk/location_edit.html'
    success_url = reverse_lazy('vms:settings')

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

class VMSKioskLocationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VMSKioskLocation
    template_name = 'kiosk/location_delete.html'
    context_object_name = 'kiosk_location'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            try:
                self.object.delete()
                messages.success(request, f'Kiosk Location named {self.object.name} has been deleted successfully.')
            except Exception as e:
                messages.error(request, e.args[0])
            return redirect(reverse('vms:settings') + '?tab=kioskLocations')

class VMSKioskTokenCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = VMSKioskToken
    form_class = VMSKioskTokenForm
    template_name = 'kiosk/token_create.html'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

    def get_success_url(self):
        success_url = reverse_lazy('vms:settings')
        query_params = {'tab': 'kioskLinks'}
        return f"{success_url}?{urlencode(query_params)}"

class VMSKioskTokenEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VMSKioskToken
    form_class = VMSKioskTokenForm
    template_name = 'kiosk/token_edit.html'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

    def get_success_url(self):
        success_url = reverse_lazy('vms:settings')
        query_params = {'tab': 'kioskTokens'}
        return f"{success_url}?{urlencode(query_params)}"
    
class VMSKioskTokenDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VMSKioskToken
    template_name = 'kiosk/token_delete.html'
    context_object_name = 'kiosk_link'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition
        
    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            try:
                self.object.delete()
                messages.success(request, f'Kiosk Link named <u>{self.object.name}</u> has been deleted successfully.')
            except Exception as e:
                messages.error(request, e.args[0])
            return redirect(reverse('vms:settings') + '?tab=kioskLocations')

class VMSKioskTokenRetrieveAPIView(generics.RetrieveAPIView):
    queryset = VMSKioskToken.objects.all()
    serializer_class = VMSKioskTokenSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class VMSAdminView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/checkin.html'
    permission_denied_message = "You do not have permission to access the VMS admin page."

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['checkins'] = VMSCheckIn.objects.all()
        context['organizations'] = VMSOrganization.objects.all()
        context['locations'] = VMSKioskLocation.objects.all()
        context['tokens'] = VMSKioskToken.objects.all()
        return context