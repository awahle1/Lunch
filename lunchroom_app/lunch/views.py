from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import json

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, "lunchroom/login.html", {"message": None})
    context = {
        'user': request.user,
    }
    return render(request, 'lunchroom/photo_home.html', context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lunchroom/login.html", {"message": "Invalid Credentials"})

def register_view(request):
    return render(request, "lunchroom/photo_register.html")

def register_action(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        if username is not None and password is not None and email is not None and first_name is not None and last_name is not None:
            newuser = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name)
            user = authenticate(request, username=username, password=password)
            #profile = Profile(userid = user.id, username = user.username)
            #profile.save()
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lunchroom/photo_register.html", {"message": "Username already in use"})

def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'lunchroom/photo_profile_two.html', context)
