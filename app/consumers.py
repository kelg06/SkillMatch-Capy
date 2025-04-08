import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope["user"]

        # Add user to the group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        # Save message to DB and get timestamp
        timestamp = await self.save_message(self.chat_id, self.user, message)

        # Broadcast message with timestamp
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': timestamp,  # Send timestamp
            }
        )

    async def chat_message(self, event):
        # Send the message and timestamp to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],  # Include timestamp
        }))

    @database_sync_to_async
    def save_message(self, chat_id, user, message):
        # Import models inside the method to ensure they are loaded when needed
        from django.contrib.auth.models import User
        from app.models import Chat, Message  # Adjust import path if needed

        chat = Chat.objects.get(id=chat_id)
        message_instance = Message.objects.create(chat=chat, sender=user, content=message)
        # Return the timestamp for the saved message
        return message_instance.created_at.strftime('%b %d, %Y %H:%M')
