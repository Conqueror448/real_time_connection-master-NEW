# backend/inventory/models.py
from django.db import models


class Item(models.Model):
    """
    The single source of truth for stock on hand.

    One row per physical SKU.  Keep it lean—add columns
    (location, unit_cost, etc.) only after the pilot proves value.
    """
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Stock-keeping unit or other unique identifier"
    )
    name = models.CharField(
        max_length=120,
        help_text="Human-readable product name"
    )
    qty = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantity on hand"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Auto-populated timestamp of last change"
    )

    class Meta:
        ordering = ["sku"]
        indexes = [
            models.Index(fields=["sku"]),
        ]
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self) -> str:
        return f"{self.sku} – {self.name}"
