# backend/inventory/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Item
from .serializers import ItemSerializer


# 🔔 Fire after every create *or* update
@receiver(post_save, sender=Item)
def broadcast_item_save(sender, instance, created, **kwargs):
    """
    Push the latest state of the Item to everyone
    connected to the "inventory" WebSocket group.
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:      # mis-configured Channels; fail silently
        return

    async_to_sync(channel_layer.group_send)(
        "inventory",
        {
            "type": "inv.update" if not created else "inv.create",
            "item": ItemSerializer(instance).data,   # JSON-ready dict
        },
    )


# 🔔 Fire after a delete so clients can remove the row
@receiver(post_delete, sender=Item)
def broadcast_item_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "inventory",
        {
            "type": "inv.delete",
            "item": {"id": instance.id},
        },
    )
