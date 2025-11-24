from django.urls import path
from .consumers import AnnouncementConsumer

websocket_urlpatterns = [
    path("ws/announcements/", AnnouncementConsumer.as_asgi()),
]
