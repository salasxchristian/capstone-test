from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, FormView
from blog.models import BlogPost
from .forms import CustomConfigForm
from constance.admin import ConstanceAdmin
from constance import config
from django.contrib.auth.models import User


class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.all().order_by('-date_added')[:3]
        return context

class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm
    change_list_template = 'admin/settings.html'

class UsersAdminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'admin/users.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

class SettingsAdminView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'admin/settings.html'
    permission_denied_message = 'You do not have permission to access this page'
    form_class = CustomConfigForm

    def test_func(self):
        return self.request.user.is_superuser  # Replace with your desired condition

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Settings have been saved successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomConfigForm()
        initial_data = {key: getattr(config, key) for key in form.CONFIG}
        context['form'] = form
        return context