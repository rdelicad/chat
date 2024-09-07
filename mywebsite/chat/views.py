from django.shortcuts import render, get_object_or_404
from .models import Room
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def home(request):
    rooms = Room.objects.all()
    return render(request, 'chat/home.html', {'rooms': rooms})

@login_required
def room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Check if the user is a member of the room
    if request.user not in room.users.all():
        error_message = "No tiene permiso para entrar en esta sala"
        return render(request, 'chat/home.html', {'error_message': error_message, 'rooms': Room.objects.all()})

    users_in_room = room.users.all()
    return render(request, 'chat/room.html', {'room': room, 'users_in_room': users_in_room})
