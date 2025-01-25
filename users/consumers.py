import json

from channels.generic.websocket import AsyncWebsocketConsumer


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
