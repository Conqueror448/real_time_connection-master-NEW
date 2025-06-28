from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()           # handshake OK

    async def receive(self, text_data):
        # send whatever we got right back
        await self.send(text_data=json.dumps({"echo": text_data}))
