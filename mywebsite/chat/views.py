from django.shortcuts import render
from .models import Room
from django.contrib.auth.decorators import login_required

def home(request):
    rooms = Room.objects.all()
    return render(request, 'chat/home.html', {'rooms': rooms})