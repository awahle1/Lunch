from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import json
from lunch.models import Table, Event, Member, Post, Comment
import time


# Create your views here.

role = ''

def mergeSort(arr):
    if len(arr) >1:
        mid = len(arr)//2 # Finding the mid of the array
        L = arr[:mid] # Dividing the array elements
        R = arr[mid:] # into 2 halves

        mergeSort(L) # Sorting the first half
        mergeSort(R) # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] > R[j]:
                arr[k] = L[i]
                i+= 1
            else:
                arr[k] = R[j]
                j+= 1
            k+= 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i+= 1
            k+= 1

        while j < len(R):
            arr[k] = R[j]
            j+= 1
            k+= 1

def get_context(user):
    context={
        'user': user,
        'propic': user.member.propic,
    }
    return(context)

def index(request):
    if not request.user.is_authenticated:
        return render(request, "lunch/login.html", {"message": None})
    context = get_context(request.user)
    posts = []
    temp = []
    tables = request.user.tables.all()
    if len(tables)>0:
        for table in tables:
            for post in table.posts.all():
                temp.append(post.ts)
        mergeSort(temp)
        for ts in temp:
            posts.append(Post.objects.get(ts = ts))
    else:
        posts = Post.objects.get()
    context['posts'] = posts
    return render(request, 'lunch/home.html', context)

def table_feed(request, tableid):
    context = get_context(request.user)
    table = Table.objects.get(id = int(tableid))
    posts = table.posts.all()
    context['posts'] = posts
    return render(request, 'lunch/home.html', context)

def explore(request):
    context = get_context(request.user)
    temp = Post.objects.all()
    posts = []
    for post in temp:
        posts.append(post)
    posts.reverse()
    context['posts'] = posts[0:30]
    temptables = []
    temptables2 = Table.objects.all()
    for table in temptables2:
        temptables.append(table)
    print(temptables)
    #for table in temptables:
    #    if request.user in table.members.all():
    #        temptables.remove(table)

    tables=[]
    for i in range(0,4):
        max=0
        maxtable=None
        for table in temptables:
            if table.members.count() > max:
                max = table.members.count()
                maxtable = table
        tables.append(maxtable)
        temptables.remove(maxtable)
    context['tables']=tables
    return render(request, 'lunch/explore.html', context)

def explore_tables(request):
    context = get_context(request.user)
    context['tables']=Table.objects.all()
    return render(request, 'lunch/table_results.html', context)

def new_post(request):
    context = get_context(request.user)
    return render(request, 'lunch/new_post.html', context)

def tables_view(request):
    context = get_context(request.user)
    return render(request, 'lunch/tables.html', context)

def profile(request):
    context = get_context(request.user)
    return render(request, 'lunch/profile.html', context)

def search_tables(request):
    search = request.POST["searchtable"]
    tables = Table.objects.filter(name__icontains=search)
    context = get_context(request.user)
    context['tables'] = tables
    return render(request, 'lunch/table_results.html', context)

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
    if request.user in members:
        members.remove(request.user)
    context = get_context(request.user)
    context['members'] = members
    return render(request, 'lunch/member_results.html', context)

def is_member(request):
    name = json.loads(request.body)['name']
    table = Table.objects.get(name = name)
    members = table.members.all()
    if request.user == table.owner:
        data = json.dumps({"status": 'Owner'})
    elif request.user in members:
        data = json.dumps({"status": 'Member'})
    else:
        data = json.dumps({"status": 'Join'})
    return HttpResponse(data, content_type='application/json')

def join(request):
    id = json.loads(request.body)['id']
    table = Table.objects.get(id = id)
    members = table.members.all()
    if request.user == table.owner:
        data = json.dumps({"status": 'Owner'})
    elif request.user in members:
        table.members.remove(request.user)
        table.save()
        data = json.dumps({"status": "Join"})
    else:
        table.members.add(request.user)
        table.save()
        data = json.dumps({"status": "Member"})
    return HttpResponse(data, content_type='application/json')

def create_table_view(request):
    context = get_context(request.user)
    return render(request, 'lunch/create_table.html', context)

def ctable_action(request):
    name=request.POST["name"]
    desc=request.POST["description"]
    table = Table(owner = request.user, name = name, description=desc)
    #Add the creator to the members list
    table.save()
    table.members.add(request.user)
    table.save()
    context = get_context(request.user)
    context['table'] = table
    tableid = table.id
    return HttpResponseRedirect(reverse("table_profile", args=[tableid]))

def table_profile(request, tableid):
    id = int(tableid)
    table = Table.objects.get(id = id)
    context = get_context(request.user)
    context['table'] = table
    return render(request, 'lunch/tableprofile.html', context)

def edit_table_profile(request, tableid):
    id = int(tableid)
    table = Table.objects.get(id = id)
    context = get_context(request.user)
    context['table'] = table
    return render(request, 'lunch/edittableprofile.html', context)

def edit_tpp(request):
    tableid = request.POST["table"]
    table = Table.objects.get(id = tableid)
    uploaded_file = request.FILES.get('propic')
    fs=FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)
    table.pp_name = uploaded_file.name
    table.save()
    context = get_context(request.user)
    context['table'] = table
    return HttpResponseRedirect(reverse("table_profile", args=[tableid]))

def edit_banner(request):
    tableid = request.POST["table"]
    table = Table.objects.get(id = tableid)
    uploaded_file = request.FILES.get('banner')
    fs=FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)
    table.banner_name = uploaded_file.name
    table.save()
    context = get_context(request.user)
    context['table'] = table
    return HttpResponseRedirect(reverse("table_profile", args=[tableid]))

def edit_description(request):
    tableid = request.POST["table"]
    table = Table.objects.get(id = tableid)
    description = request.POST['description']
    table.description = description
    table.save()
    context = get_context(request.user)
    context['table'] = table
    return HttpResponseRedirect(reverse("table_profile", args=[tableid]))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lunch/login.html", {"message": "Invalid Credentials"})

def logout_view(request):
    logout(request)
    return render(request, "lunch/login.html")

def register_view(request):
    return render(request, "lunch/register.html")

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
        return render(request, "lunch/role.html")
    else:
        return render(request, "lunch/register.html", {"message": "Username already in use"})

def role_view(request):
    global role
    role = request.POST["role"]
    if role == 'Student':
        return render(request, "lunch/yog.html")
    else:
        return render(request, "lunch/title.html")

def create_member_view(request):
    if role == 'Student':
        yog = request.POST["yog"]
        member = Member(role='Student', user=request.user, yog=yog)
        member.save()
    else:
        title = request.POST["title"]
        member = Member(role='Teacher', user=request.user, title=title)
        member.save()
    return HttpResponseRedirect(reverse("profile"))

def show_post(request, postid):
    context=get_context(request.user)
    postid = int(postid)
    post = Post.objects.get(id = postid)
    context['post']=post
    return render(request, 'lunch/post.html', context)

def comment(request):
    comment = request.POST['comment']
    postid = request.POST['postid']
    newcomment = Comment(text=comment, author=request.user, mauthor=request.user.member, ts=time.time())
    newcomment.save()
    post = Post.objects.get(id=postid)
    post.comments.add(newcomment)
    post.save()
    return HttpResponseRedirect(reverse("show_post", args=[postid]))

def show_tables(request, username):
    context=get_context(request.user)
    context['tables']=User.objects.get(username=username).tables.all()
    return render(request, 'lunch/table_results.html', context)

def user_profile(request, username):
    user = User.objects.get(username=username)
    context=get_context(user)
    return render(request, 'lunch/user_profile.html', context)

def postpic(request):
    context=get_context(request.user)
    uploaded_file = request.FILES.get('propic')
    text = request.POST['text']
    table = request.POST['table']
    table = Table.objects.get(name=table)
    fs=FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)
    member = Member.objects.get(user = request.user)
    post = Post(text=text, picture_name=uploaded_file.name,author=request.user, ts = time.time(), auth_pp=member.propic)
    post.save()
    post.table = table
    post.save()
    context['post']=post
    return render(request, 'lunch/post.html', context)

def propic(request):
    user=request.user
    member = Member.objects.get(user=user)
    uploaded_file = request.FILES.get('propic')
    fs=FileSystemStorage()
    fs.save(uploaded_file.name, uploaded_file)
    member.propic = uploaded_file.name
    member.save()
    context=get_context(request.user)
    return HttpResponseRedirect(reverse("profile"))
