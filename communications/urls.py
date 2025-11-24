from django.urls import path
from . import views

app_name = "communications"

urlpatterns = [
    path("hr/", views.hr_dashboard, name="hr_dashboard"),

    # HR creates an announcement
    path("api/post/", views.post_announcement, name="post_announcement"),

    # Dashboard fetches announcements
    path("api/get/", views.get_announcements, name="get_announcements"),
]
