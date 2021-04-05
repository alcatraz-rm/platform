from django.contrib import admin
from django.contrib.auth import views as dj_auth_views
from django.urls import path

from authorization import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path("login/", dj_auth_views.LoginView.as_view(), name="login"),
    path("login/", auth_views.user_login_view, name="login"),
    path("sing-up/", auth_views.sing_up_view, name="sing-up"),
]
