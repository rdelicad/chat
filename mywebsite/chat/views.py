from django.shortcuts import render
from .models import Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    rooms = Room.objects.all()
    return render(request, 'chat/home.html', {'rooms': rooms})

@login_required
def room(request, room_id):
    try:
        room = request.user.rooms_joined.get(id=room_id) # Check if user is in the room

    except Room.DoesNotExist:
        error_message = "No tiene permiso para entrar en esta sala" # If not, return 403 Forbidden, cambiar por pagina de error
        return render(request, 'chat/home.html', {'error_message': error_message, 'rooms': Room.objects.all()})
    
    return render(request, 'chat/room.html', {'room': room})