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
    table = models.ManyToManyField(Table, blank=True, related_name='posts')
    author = models.ManyToManyField(User, blank=True, related_name='posts')
