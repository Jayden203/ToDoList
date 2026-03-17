from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/new/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task_status'),
    path('categories/', views.categories_view, name='categories'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('analytics/', views.analytics, name='analytics'),
    path("tasks/<int:task_id>/toggle-ajax/", views.toggle_task_status_ajax, name="toggle_task_status_ajax"),
]