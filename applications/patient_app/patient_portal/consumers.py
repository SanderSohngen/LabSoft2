import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extracting parameters from the URL route
        self.patient_id = self.scope['url_route']['kwargs']['patient_id']
        self.profession = self.scope['url_route']['kwargs']['profession']
        self.professional_id = self.scope['url_route']['kwargs']['professional_id']
        
        # Create a unique room group name
        self.room_group_name = f'chat_{self.patient_id}_{self.profession}_{self.professional_id}'
        print(f"Connecting to {self.room_group_name}")

        # Add current channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Logging the disconnect
        print(f"Disconnecting from {self.room_group_name}")
        # Remove the channel from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        print(self.scope['client'][0])

        if self.scope['client'][0] == 'ec2-52-67-134-153.sa-east-1.compute.amazonaws.com' :
            origin = 'internal' 
        elif self.scope['client'][0] == '127.0.0.1' :
            origin = 'internal' 
        else :
            origin = 'external'

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'origin': origin
            }
        )

    async def chat_message(self, event):
        # Extract the message and origin from the event
        message = event['message']
        origin = event.get('origin', 'unknown')  # Default to 'unknown' if not specified

        print(f"Broadcast message: {message} from {origin} to group {self.room_group_name}")

        # Send the message over WebSocket including the origin
        await self.send(text_data=json.dumps({
            'message': message,
            'origin': origin  # Include the origin in the message sent to the client
        }))