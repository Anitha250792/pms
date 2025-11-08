from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # Task list
    path("", views.task_list, name="task_list"),

    # Manager: view team member’s tasks
    path("member/<int:user_id>/", views.task_list, name="task_list_for_member"),

    # Task creation
    path("create/", views.task_create, name="task_create"),

    # Task detail (keep this **after** AJAX URLs)
    path("<int:pk>/", views.task_detail, name="task_detail"),

    # AJAX: update status
    path("<int:pk>/update-status/", views.update_task_status, name="update_task_status"),

    # AJAX: update completion
    path("<int:pk>/update-completion/", views.update_task_completion, name="update_task_completion"),

    # Edit/Delete
    path("<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
    path('<int:pk>/view/', views.task_detail_readonly, name='task_detail_readonly'),

]
