from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *

# Frameworks like Django allow us to take advantage of generic views such as CreateView, ListView, UpdateView, and DeleteView to quickly create views for our models
# and abstract common pattersn to a higher level, making the application easier to develop, maintain and scale.

# ResourceLinkCreateView is a view that allows users to create a new link
# An example of implementing industry appropriate security measures such as using the PermissionRequiredMixin
# to ensure that only users with the correct permissions can create a new link
class ResourceLinkCreateView(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
    model = ResourceLink
    form_class = ResourceLinkForm 
    template_name = 'link_create.html'
    success_url = reverse_lazy('resources:links')
    permission_required = 'resources.add_resourcelink'
    permission_denied_message = 'You do not have permission to create a Resource Link'   

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            category_id = self.request.GET.get('category')
            if category_id:
                kwargs['category_id'] = category_id
            return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_modified_by = self.request.user
        messages.success(self.request, f'Link named {form.instance.title} has been created successfully.')
        return super().form_valid(form)
    
# ResourceLinkListView is a view that displays all links    
class ResourceLinkListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResourceLinkCategory
    template_name = 'links.html'
    context_object_name = 'link_categories'
    permission_required = 'resources.view_resourcelink'
    permission_denied_message = 'You do not have permission to view Resource Links'   

    def get_queryset(self):
        return ResourceLinkCategory.objects.all().order_by('name')

# LinkEditView is a view that allows users to edit an existing link
class ResourceLinkEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ResourceLink
    form_class = ResourceLinkForm
    permission_required = 'resources.change_resourcelink'
    permission_denied_message = 'You do not have permission to edit Resource Links'
    template_name = 'link_edit.html'
    success_url = reverse_lazy('resources:links')

# LinkDeleteView is a view that allows users to delete an existing link
class ResourceLinkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ResourceLink
    permission_required = 'network_portal.delete_resourcelink'
    permission_denied_message = 'You do not have permission to delete links'
    template_name = 'link_delete.html'
    context_object_name = 'link'

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            try:
                self.object.delete()
                messages.success(request, f'Link named {self.object.title} has been deleted successfully.')
            except Exception as e:
                messages.error(request, e.args[0])
            return redirect('resources:links')

class ResourceLinkCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ResourceLinkCategory
    form_class = ResourceLinkCategoryForm
    permission_required = 'resources.add_resourcelinkcategory'
    permission_denied_message = 'You do not have permission to create Resource Link Categories'
    template_name = 'link_category_create.html'
    success_url = reverse_lazy('resources:categories')

    def form_valid(self, form):
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)
    
class ResourceLinkCategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ResourceLinkCategory
    permission_required = 'resources.view_resourcelinkcategory'
    permission_denied_message = 'You do not have permission to view Resource Link Categories'
    template_name = 'link_categories.html'

    def get_queryset(self):
        return ResourceLinkCategory.objects.order_by('-last_modified')

class ResourceLinkCategoryEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ResourceLinkCategory
    form_class = ResourceLinkCategoryForm
    permission_required = 'resources.change_resourcelinkcategory'
    permission_denied_message = 'You do not have permission to edit Resource Link Categories'
    template_name = 'link_category_edit.html'
    success_url = reverse_lazy('resources:categories')

    def form_valid(self, form):
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)
    
class ResourceLinkCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ResourceLinkCategory
    permission_required = 'resources.delete_resourcelinkcategory'
    permission_denied_message = 'You do not have permission to delete Resource Link Categories'
    template_name = 'link_category_delete.html'
    context_object_name = 'link_category'    

    def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            try:
                self.object.delete()
                messages.success(request, f'Resource Link Category named {self.object.name} has been deleted successfully.')
            except Exception as e:
                messages.error(request, e.args[0])
            return redirect('resources:categories')