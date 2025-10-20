"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'backend' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Standard Django ASGI application
django_asgi_app = get_asgi_application()

# Optional: If you want WebSocket support later (Django Channels), uncomment the following:
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import your_app.routing
#
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             your_app.routing.websocket_urlpatterns
#         )
#     ),
# })

# For now, standard HTTP ASGI application
application = django_asgi_app
