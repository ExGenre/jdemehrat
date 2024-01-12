from django.urls import path
from .views import register, profile, profile_list
from django.contrib.auth.views import LogoutView
from .views import user_login

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile_list/', profile_list, name='profile_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_login/', user_login, name='user_login'),
]
