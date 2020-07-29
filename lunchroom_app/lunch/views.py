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
    return render(request, 'lunchroom/home.html', context)

def profile(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/profile.html', context)

def tables_view(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/tables.html', context)

def explore(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/explore.html', context)

def search_tables(request):
    search = request.POST["searchtable"]
    tables = Table.objects.filter(name__icontains=search)
    context = get_context(request.user)
    context['tables'] = tables
    return render(request, 'lunchroom/table_results.html', context)

def search_members(request):
    #Get the search string and preform various queries
    search = request.POST['searchmember']
    r1 = User.objects.filter(first_name__icontains=search)
    r2 = User.objects.filter(last_name__icontains=search)
    if ' ' in search:
        s1 = search[:search.index(' ')]
        s2 = search[search.index(' ')+1:]
        r3 = User.objects.filter(first_name__icontains=s1)
        r4 = User.objects.filter(last_name__icontains=s2)
        results = r1.union(r2, r3, r4)
    else:
        results = r1.union(r2)
    members = []
    #Turn the quereyset into a normal list
    for value in results:
        members.append(value)
    context = get_context(request.user)
    context['members'] = members
    return render(request, 'lunchroom/member_results.html', context)

def create_table_view(request):
    context = get_context(request.user)
    return render(request, 'lunchroom/create_table.html', context)

def ctable_action(request):
    name=request.POST["name"]
    desc=request.POST["description"]
    table = Table(owner = request.user, name = name, description=desc)
    #Add the creator to the members list
    table.members.add(request.user)
    table.save()
    context = get_context(request.user)
    context['table'] = table
    return render(request, 'lunchroom/tableprofile.html', context)

def table_profile(request, tableid):
    id = int(tableid)
    table = Table.objects.get(id = id)
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
    return render(request, "lunchroom/register.html")

def register_action(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        #Making sure all fields are filled, otherwise send an error message
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
        return render(request, "lunchroom/register.html", {"message": "Username already in use"})

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
