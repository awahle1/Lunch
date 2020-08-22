from django.contrib import admin

from .models import Member, Table, Event, Post, Comment
# Register your models here.
admin.site.register(Member)
admin.site.register(Table)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Comment)
