from django.urls import path
from . import views
from . import api_views  # Required because you are using project_api

app_name = 'projects'

urlpatterns = [
    # Main Project CRUD
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Read-only view
    path('<int:pk>/view/', views.project_detail_readonly, name='project_detail_readonly'),

    # AJAX Status Updates
    path('<int:pk>/update_status_ajax/', views.update_status_ajax, name='update_status_ajax'),
    path('<int:pk>/update_completion_ajax/', views.update_completion_ajax, name='update_completion_ajax'),

    # API endpoint
    path('api/<int:pk>/', api_views.project_api, name='project_api'),

    # Assign members
    path('<int:project_id>/assign/', views.assign_project_ajax, name='assign_project_ajax'),
    path('<int:project_id>/assign/<int:user_id>/', views.assign_member, name='assign_member'),

    # Delete image
    path('delete-image/<int:image_id>/', views.delete_project_image, name='delete_project_image'),
]
