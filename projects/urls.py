from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    # List & Create
    path("", views.project_list, name="project_list"),
    path("create/", views.project_create, name="project_create"),

    # Detail Views (Editable + Read-only)
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path("<int:pk>/view/", views.project_detail_readonly, name="project_detail_readonly"),

    # Edit / Delete
    path("<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("<int:pk>/delete/", views.project_delete, name="project_delete"),

    # Ajax Status + Completion Updates
    path("<int:project_id>/update-status/", views.update_status_ajax, name="update_status_ajax"),
    path("<int:project_id>/update-completion/", views.update_completion_ajax, name="update_completion_ajax"),

    # Assign project
    path("<int:project_id>/assign/", views.assign_project_ajax, name="assign_project_ajax"),
    path("<int:project_id>/assign/<int:user_id>/", views.assign_member, name="assign_member"),

    # Delete image
    path("delete-image/<int:image_id>/", views.delete_project_image, name="delete_project_image"),
]
