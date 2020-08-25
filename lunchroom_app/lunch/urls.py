from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path("", views.index, name="index"),
    path("new_post", views.new_post, name="new_post"),
    path("explore", views.explore, name="explore"),
    path("tables", views.tables_view, name="tables"),
    path("profile", views.profile, name="profile"),

    path("tablefeed/<str:tableid>", views.table_feed, name="table_feed"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("register_action", views.register_action, name="register_action"),
    path("role", views.role_view, name="role"),
    path("create_member", views.create_member_view, name = "create_member"),

    path("create_table", views.create_table_view, name = "create_table"),
    path("ctable_action", views.ctable_action, name="ctable_action"),

    path("search_tables", views.search_tables, name='search_tables'),
    path("search_members", views.search_members, name='search_members'),
    path("tables/<str:tableid>", views.table_profile, name = "table_profile"),
    path("tables/<str:tableid>/edit", views.edit_table_profile, name = "edit_table_profile"),

    path("edit_tpp", views.edit_tpp, name="edit_tpp"),
    path("edit_banner", views.edit_banner, name="edit_banner"),
    path("edit_description", views.edit_description, name="edit_description"),

    path("posts/<str:postid>", views.show_post, name = "show_post"),
    path("comment", views.comment, name="comment"),

    path("usertables/<str:username>", views.show_tables, name = "show_tables"),
    path("users/<str:username>", views.user_profile, name="user_profile"),

    path('is_member', views.is_member, name="in_member"),
    path('join', views.join, name="join"),

    path('postpic', views.postpic, name='postpic'),
    path('propic', views.propic, name='propic'),

    path('explore_tables', views.explore_tables, name='explore_tables'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
