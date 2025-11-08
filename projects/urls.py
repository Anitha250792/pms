from django.urls import path
from . import views
from . import api_views

app_name = 'projects'  # ✅ Important for namespacing

urlpatterns = [
    
    path('', views.project_list, name='project_list'), 
    path('<int:pk>/', views.project_detail, name='project_detail'),                              # List all projects
    path('create/', views.project_create, name='project_create'),     # Create new project
    path('<int:pk>/', views.project_detail, name='project_detail'),   # ✅ View a single project (added)
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),  # Edit project
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),  # Delete project
    
    path('<int:pk>/update_status_ajax/', views.update_status_ajax, name='update_status_ajax'),
    path('<int:pk>/update_completion_ajax/', views.update_completion_ajax, name='update_completion_ajax'),
    path("update-status/<int:project_id>/", views.update_status_ajax, name="update_status_ajax"),
    path("update-completion/<int:project_id>/", views.update_completion_ajax, name="update_completion_ajax"),
    path('update/<int:pk>/', views.project_edit, name='project_update'),
    path("delete-image/<int:image_id>/", views.delete_project_image, name="delete_project_image"),
    path('<int:pk>/view/', views.project_detail_readonly, name='project_detail_readonly'),

     path("api/<int:pk>/", api_views.project_api, name="project_api"),
    path("<int:project_id>/update-status/", views.update_status_ajax, name="update_status_ajax"),
    path("<int:project_id>/update-completion/", views.update_completion_ajax, name="update_completion_ajax"),
    path("<int:project_id>/assign/", views.assign_project_ajax, name="assign_project_ajax"),

    path("<int:project_id>/assign/<int:user_id>/", views.assign_member, name="assign_member"),


]
