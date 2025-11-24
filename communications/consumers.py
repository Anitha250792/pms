import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AnnouncementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("announcements", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("announcements", self.channel_name)

    async def announce_message(self, event):
        await self.send(text_data=json.dumps({
            "message": {
                "id": event["id"],
                "sender": event["sender"],
                "content": event["content"],
                "created_at": event["created_at"],
            }
        }))
