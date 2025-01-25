import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer handles WebSocket connections for a chat application.

    Methods
    -------
    connect():
        Handles the WebSocket connection establishment.
        Authenticates the user and adds the consumer to a channel group.

    disconnect(close_code):
        Handles the WebSocket disconnection.
        Removes the consumer from the channel group.

    receive(text_data):
        Handles incoming WebSocket messages.
        Parses the message, saves it to the database, and broadcasts it to the group.

    chat_message(event):
        Handles the custom "chat_message" event.
        Sends the message content to the WebSocket client.
    """

    async def connect(self):
        print("connected")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name

        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("message", "")
        sender_id = self.scope["user"].id
        splitted = self.room_name.split("_")
        user_a_id, user_b_id = splitted[1], splitted[2]

        if str(sender_id) == user_a_id:
            receiver_id = user_b_id
        else:
            receiver_id = user_a_id

        msg = await sync_to_async(Message.objects.create)(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            room_name=self.room_name,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "content": content,
                "timestamp": str(msg.timestamp),
            },
        )

    async def chat_message(self, event):
        """
        Metodo handler per l'evento custom "chat_message".
        Invia il contenuto sul WebSocket client.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "sender_id": event["sender_id"],
                    "receiver_id": event["receiver_id"],
                    "content": event["content"],
                    "timestamp": event["timestamp"],
                }
            )
        )


class NotificationsConsumer(AsyncWebsocketConsumer):
    """
    NotificationsConsumer is an AsyncWebsocketConsumer that handles WebSocket connections
    for sending notifications to authenticated users.

    Methods:
        Handles the WebSocket connection event. If the user is authenticated, adds the
        user to a group based on their user ID and accepts the connection. If not authenticated,
        closes the connection.

        Handles the WebSocket disconnection event. If the user is not anonymous, removes
        the user from the group based on their user ID.

        Sends a notification to the WebSocket client. The notification data is expected
        to be in the `event` dictionary under the key "notification".
    """

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if not self.scope["user"].is_anonymous:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(text_data=json.dumps({"notification": notification}))
