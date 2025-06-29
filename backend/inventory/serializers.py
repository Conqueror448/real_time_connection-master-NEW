from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # expose everything you need on the front-end
        fields = ["id", "sku", "name", "qty", "updated_at"]
