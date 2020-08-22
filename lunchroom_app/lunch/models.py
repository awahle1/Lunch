from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Member(models.Model):
    role = models.CharField(
        max_length = 7,
        choices = [('Teacher', 'Student')],
        default='Student',
    )
    propic = models.CharField(
        max_length = 200,
        default='defaultpropic.png',
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member', null=True)
    yog = models.CharField(
        max_length=4,
        default = ''
    )
    title = models.CharField(
        max_length=4,
        default = ''
    )
    def __str__(self):
        return (self.user.first_name + " "+ self.user.last_name)

class Comment(models.Model):
    text = models.CharField(
        max_length=300,
        default = ''
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    mauthor = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='comments')
    ts = models.IntegerField(
        default = 0,
        null = True,
        blank=True
    )

class Event(models.Model):
    name = models.CharField(
        max_length=50,
        default = ''
    )
    description = models.CharField(
        max_length = 200,
        default = ''
    )
    hostuser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    def __str__(self):
        return (self.name)

class Table(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ownedtables')
    members = models.ManyToManyField(User, blank=True, related_name='tables')
    events = models.ManyToManyField(Event, blank=True, related_name='host')
    name = models.CharField(
        max_length=50,
        default = ''
    )
    description = models.CharField(
        max_length = 200,
        default = ''
    )
    banner_name = models.CharField(
        max_length = 200,
        default = ''
    )
    pp_name = models.CharField(
        max_length = 200,
        default = ''
    )
    def __str__(self):
        return (self.name)

class Post(models.Model):
    text = models.CharField(
        max_length=300,
        default = ''
    )
    picture_name = models.CharField(
        max_length=300,
        default = ''
    )
    auth_pp = models.CharField(
        max_length=300,
        default = ''
    )
    ts = models.IntegerField(
        default = 0,
        null = True,
        blank=True
    )
    comments = models.ManyToManyField(Comment, blank=True, related_name='post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='posts', null=True)
