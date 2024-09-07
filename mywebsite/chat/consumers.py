import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Room

class ChatConsumer(WebsocketConsumer):
    connected_users = set()

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'sala_chat_{self.id}'
        self.user = self.scope['user']
        print("Conexion establecida al grupo: ", self.room_group_name)
        print("Conexion establecida con el channel_name: ", self.channel_name)

        # Add user to connected users set
        self.connected_users.add(self.user.username)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # Notify group about the new user
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.user.username,
            }
        )

        # Send the list of currently connected users to the new user
        self.send(text_data=json.dumps({
            'type': 'connected_users',
            'users': list(self.connected_users),
        }))

    def disconnect(self, close_code):
        print("disconnected")

        # Remove user from connected users set
        self.connected_users.discard(self.user.username)

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Notify group about the user leaving
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.user.username,
            }
        )

    def receive(self, text_data):
        print("received")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Obtenemos el ID del usuario que envia el mensaje
            if self.user.is_authenticated:
                sender_id = self.scope['user'].id
            else:
                None
            if sender_id:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'datatime': timezone.localtime(timezone.now()).strftime('%H:%M'),
                        'sender_id': sender_id
                    }
                )
            else:
                print("Usuario no autenticado. Ignorando mensaje")

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar el mensaje: ', e)
        except KeyError as e:
            print('Hubo un error al acceder a una clave del diccionario: ', e)
        except Exception as e:
            print('Hubo un error inesperado: ', e)

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        datatime = event['datatime']
        sender_id = event['sender_id']

        current_user_id = self.scope['user'].id
        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'datatime': datatime,
                'sender_id': sender_id
            }))

    def user_join(self, event):
        username = event['username']
        self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': username,
        }))

    def user_leave(self, event):
        username = event['username']
        self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': username,
        }))
