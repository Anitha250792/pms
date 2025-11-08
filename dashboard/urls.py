from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Main /dashboard/ – just redirects to global read-only
    path("", views.dashboard, name="dashboard"),

    # 🌍 Default Global Dashboard (Home for all users)
    path("global/", views.global_dashboard, name="global_dashboard"),

    # Old paths still available
    path("", views.global_dashboard, name="dashboard"),

    # Role Selection Page
    path("select-role/", views.select_role, name="select_role"),

    # HR Dashboard
    path("hr/", views.hr_dashboard, name="hr_dashboard"),

    # Design Team Dashboard
    path("design/", views.design_dashboard, name="design_dashboard"),

    # Team Member Individual Dashboard
    path("member/<int:user_id>/", views.member_dashboard_view, name="member_dashboard"),

    # Manager dashboard
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
]
