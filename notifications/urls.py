from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="list"),  # 👈 New Main List Page
    path("unread/", views.get_unread_notifications, name="unread"),
    path("read/<int:note_id>/", views.mark_as_read, name="mark_read"),
]
