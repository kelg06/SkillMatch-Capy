import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get the default ASGI application
django_asgi_app = get_asgi_application()

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Just use the default ASGI application (no WhiteNoise here)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
