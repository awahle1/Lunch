from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("tables", views.tables_view, name="tables"),
    path("profile", views.profile, name="profile"),
    path("explore", views.explore, name="explore"),

    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("register_action", views.register_action, name="register_action"),
    path("role", views.role_view, name="role"),
    path("create_member", views.create_member_view, name = "create_member"),

    path("create_table", views.create_table_view, name = "create_table"),
    path("ctable_action", views.ctable_action, name="ctable_action"),

    path("search_tables", views.search_tables, name='search_tables'),
    path("search_members", views.search_members, name='search_members'),
    path("tables/<str:tableid>", views.table_profile, name = "table_profile"),
    ]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
