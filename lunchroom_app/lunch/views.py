from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import json
from lunch.models import Table, Event, Member


# Create your views here.

role = ''

def get_context(user):
    context={
        'user': user
    }
    return(context)

def index(request):
    if not request.user.is_authenticated:
        return render(request, "lunchroom/login.html", {"message": None})
    context = get_context(request.user)
    return render(request, 'lunchroom/photo_home.html', context)

def profile(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/photo_profile_two.html', context)

def tables_view(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/tables.html')

def create_table_view(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/create_table.html', context)

def ctable_action(request):
    name=request.POST["name"]
    desc=request.POST["description"]
    table = Table(owner = request.user, name = name, description=desc)
    table.members.add(request.user)
    table.save()
    context = get_context(request.user)
    context['table'] = table
    return render(request, 'lunchroom/tableprofile.html', context)


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
            login(request, user)
        return render(request, "lunchroom/role.html")
    else:
        return render(request, "lunchroom/photo_register.html", {"message": "Username already in use"})

def role_view(request):
    global role
    role = request.POST["role"]
    if role == 'Student':
        return render(request, "lunchroom/yog.html")
    else:
        return render(request, "lunchroom/title.html")

def create_member_view(request):
    if role == 'Student':
        yog = request.POST["yog"]
        member = Member(role='Student', info=request.user, yog=yog)
        member.save()
    else:
        title = request.POST["title"]
        member = Member(role='Teacher', info=request.user, title=title)
        member.save()
    return HttpResponseRedirect(reverse("profile"))
