from django.urls import re_path
from . import consumers

# Definimos las rutas de WebSocket para el chat.
websocket_urlpatterns = [
    # Ruta para los chats, acepta cualquier nombre de sala
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
