from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1) put every socket in the same group
        self.group_name = "echo"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 2) tidy-up
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # 3) broadcast whatever we got
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast",      # ↙ handler name below
                "message": text_data,
            },
        )

    # 4) handler that the group dispatcher calls
    async def broadcast(self, event):
        await self.send(text_data=json.dumps({"echo": event["message"]}))
