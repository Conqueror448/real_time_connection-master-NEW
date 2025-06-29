from channels.generic.websocket import AsyncWebsocketConsumer

GROUP_NAME = "inventory"          # must match the group_send() call in signals.py


class InventoryConsumer(AsyncWebsocketConsumer):
    # ---- lifecycle ---------------------------------------------------------

    async def connect(self):
        """
        1. A browser hits ws://…/ws/inventory/
        2. We accept the socket and join the shared “inventory” group
        """
        await self.channel_layer.group_add(GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Leave the group so we don’t leak channels when the tab closes."""
        await self.channel_layer.group_discard(GROUP_NAME, self.channel_name)

    # ---- (optional) incoming messages from the browser ---------------------
    # For this MVP the WebSocket is **read-only**, so we ignore anything the
    # client sends.  You can enable edits later by implementing receive_json().
    async def receive_json(self, content, **kwargs):
        pass

    # ---- handlers for broadcasts coming *from* Django signals --------------
    # (Channels calls the handler whose name matches event["type"].)
    async def inv_create(self, event):
        await self.send_json({
            "action": "create",
            "item": event["item"],
        })

    async def inv_update(self, event):
        await self.send_json({
            "action": "update",
            "item": event["item"],
        })

    async def inv_delete(self, event):
        await self.send_json({
            "action": "delete",
            "item": event["item"],
        })
