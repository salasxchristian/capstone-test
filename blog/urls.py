from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('create-post/', BlogPostCreateView.as_view(), name='create_post'),
    path('posts/', BlogPostListView.as_view(), name='posts'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', BlogPostEditView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
]