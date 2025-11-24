from django.urls import path
from . import views

app_name = "design"

urlpatterns = [
    path("", views.design_dashboard, name="design_dashboard"),
    path("<int:project_id>/upload/", views.upload_design, name="upload_design"),
    path("<int:project_id>/detail/", views.design_detail, name="design_detail"),
]
