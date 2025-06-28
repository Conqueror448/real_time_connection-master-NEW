"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os, django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import realtime.routing          # <- we’ll add this app next

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "app.settings.production"     # production settings
)
django.setup()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(realtime.routing.websocket_urlpatterns),
    }
)
