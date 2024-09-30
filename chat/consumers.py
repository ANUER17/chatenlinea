import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()  # Desconectar si el usuario no está autenticado
        else:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            # Añadir el consumidor al grupo de la sala
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Notificar que el usuario está en línea en todos los grupos
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.scope['user'].username,
                    'status': 'online'
                }
            )

            await self.accept()  # Aceptar la conexión WebSocket

    async def disconnect(self, close_code):
        # Abandonar el grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notificar que el usuario está desconectado en todos los grupos
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'username': self.scope['user'].username,
                'status': 'offline'
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender = self.scope['user']  # Usuario autenticado que envía el mensaje
        recipient_username = self.room_name  # El nombre de la sala es el nombre del receptor

        if not message.strip():
            return  # No enviar mensajes vacíos

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return  # Si no se encuentra el receptor, no hacer nada

        # Guardar el mensaje en la base de datos
        try:
            Message.objects.create(
                sender=sender,
                recipient=recipient,
                content=message,
                is_read=False  # Marcar el mensaje como no leído inicialmente
            )
        except Exception as e:
            print(f"Error guardando el mensaje: {e}")
            return

        # Enviar el mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Enviar el mensaje con el remitente al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def user_status(self, event):
        username = event['username']
        status = event['status']

        # Enviar el estado del usuario (en línea o desconectado) a los usuarios conectados
        await self.send(text_data=json.dumps({
            'username': username,
            'status': status
        }))
