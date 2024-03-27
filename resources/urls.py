from django.urls import path
from .views import *

app_name = 'resources'

urlpatterns = [
    path('links/', ResourceLinkListView.as_view(), name='links'),
    path('create-link/', ResourceLinkCreateView.as_view(), name='create_link'),
    path('link/<int:pk>/edit/', ResourceLinkEditView.as_view(), name='link_edit'),
    path('link/<int:pk>/delete/', ResourceLinkDeleteView.as_view(), name='link_delete'),
    path('create-linkcategory/', ResourceLinkCategoryCreateView.as_view(), name='create_link_category'),
    path('link/categories/', ResourceLinkCategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/edit/', ResourceLinkCategoryEditView.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', ResourceLinkCategoryDeleteView.as_view(), name='category_delete'),
]