from django.contrib import admin
from django.urls import path
from links.views import home, register, login_view, logout_view, dashboard, user_linktree, search_profiles, user_directory

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),

    
    path("search/", search_profiles, name="search_profiles"),
    path("users/", user_directory, name="user_directory"),

    path("<str:username>/", user_linktree, name="user_linktree"),
]