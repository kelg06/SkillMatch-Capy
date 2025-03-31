import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from app.routing import websocket_urlpatterns  # Import routing from your app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StartUp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)  # Use imported routing
    ),
})
