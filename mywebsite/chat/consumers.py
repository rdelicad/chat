from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = set()

    async def connect(self):
        # Extraemos el room_id desde los argumentos de la URL correctamente
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'sala_chat_{self.room_id}' 
        self.user = self.scope['user']

        if self.user.is_authenticated:
            self.username = self.user.username
        else:
            self.username = 'Anonimo'
            
        print("Conexión establecida al grupo:", self.room_group_name)
        print("Conexión establecida con el channel_name:", self.channel_name)

        # Añadir el usuario a la lista de usuarios conectados
        self.connected_users.add(self.user.username)

        # Agregar al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notificar al grupo sobre el nuevo usuario
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.username,
            }
        )

        # Enviar la lista de usuarios conectados al nuevo usuario
        await self.send(text_data=json.dumps({
            'type': 'connected_users',
            'users': list(self.connected_users),
        }))

    async def disconnect(self, close_code):
        print("Desconectado")

        # Eliminar el usuario de la lista de usuarios conectados
        self.connected_users.discard(self.user.username)

        # Eliminar del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notificar al grupo sobre el usuario que salió
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.user.username,
            }
        )

    async def receive(self, text_data):
        print("Recibido")
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Obtenemos el ID del usuario que envía el mensaje
            if self.user.is_authenticated:
                sender_id = self.user.id
            else:
                sender_id = None

            if sender_id and message:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.username,
                        'datetime': timezone.localtime(timezone.now()).strftime('%H:%M'),
                        'sender_id': sender_id
                    }
                )
            else:
                print("Usuario no autenticado. Ignorando mensaje")

        except json.JSONDecodeError as e:
            print('Error al decodificar el mensaje:', e)
        except KeyError as e:
            print('Error al acceder a una clave del diccionario:', e)
        except Exception as e:
            print('Error inesperado:', e)

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        current_user_id = self.user.id
        if sender_id != current_user_id:
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'datetime': datetime,
                'sender_id': sender_id
            }))

    async def user_join(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': username,
        }))
        

    async def user_leave(self, event):
        username = event['username']
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': username,
        }))
