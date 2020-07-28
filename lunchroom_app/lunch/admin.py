from django.contrib import admin

from .models import Member, Table, Event
# Register your models here.
admin.site.register(Member)
admin.site.register(Table)
admin.site.register(Event)
