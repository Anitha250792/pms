from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def notify(user, message, link=None):
    Notification.objects.create(
        user=user,
        message=message,
        link=link
    )

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"notif_{user.id}",
        {
            "type": "send_notification",
            "message": message,
            "link": link or "",
        }
    )
