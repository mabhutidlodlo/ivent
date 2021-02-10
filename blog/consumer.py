# chat/consumers.py
import os

import json
import asyncio
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import Profile
from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def get_all_users(self, id):
        profile = Profile.objects.get(id=id)

        return profile.following.all()

    async def connect(self):
        id = self.scope['url_route']['kwargs']['id']
        token = self.scope['url_route']['kwargs']['token']
        #token_exists then  add the channel_layer to the group
        verify = await database_sync_to_async(self.check_token)(token)
        group_name = 'new_group'
        if verify :

            for group in await self.get_all_users(id):

        # Join room group
                    await self.channel_layer.group_add(
                    group.username,
                    self.channel_name
                    )

        await self.accept()


    async def disconnect(self):
        for group in await self.get_all_users(id):
        # Leave all room group
            await self.channel_layer.group_discard(
                    group.username,
                    self.channel_name
                    )

    # Receive message from WebSocket
    async def receive(self, text_data):

        data = json.load(text_data)
        if data.command == 'unfollow':
            await self.unfollow(data.username)

        if data.command == "follow":
            await self.follow(data.username)

    async def unfollow(self, group_name):
        await self.channel_layer.group_discard(
        group_name,
        self.channel_name
        )

    async def follow(self, group_name):
        await self.channel_layer.group_add(
        group_name,
        self.channel_name
        )
#receive command from websocket when you unfollow or follow
#you will immediately be added to the group of the person you follow



    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


    def check_token(self,token):

        return Token.objects.get(key = token)
