from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from .models import BlogPost
from .forms import BlogPostForm

class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    permission_required = 'blog.add_blogpost'
    permission_denied_message = 'You do not have permission to create a Blog Post'
    template_name = 'create_post.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

class BlogPostListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BlogPost
    permission_required = 'blog.view_blogpost'
    permission_denied_message = 'You do not have permission to view Blog Posts'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5  # Display 5 posts per page

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-date_added')

class BlogPostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = BlogPost
    permission_required = 'blog.view_blogpost'
    permission_denied_message = 'You do not have permission to view Blog Posts'
    template_name = 'post_detail.html'
    context_object_name = 'post'

class BlogPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    context_object_name = 'post'
    permission_denied_message = 'You do not have permission to edit this Blog Post'
    template_name = 'post_edit.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.created_by or self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'post_delete.html'
    context_object_name = 'post'
    permission_denied_message = 'You do not have permission to delete this Blog Post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.created_by or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title  # Capture the title before deletion for the message
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f'Blog Post named <u>{title}</u> has been deleted successfully.')
        return redirect(success_url)

    def get_success_url(self):
        return reverse('blog:posts')