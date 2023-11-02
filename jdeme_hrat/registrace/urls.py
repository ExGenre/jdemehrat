from django.urls import path
from .views import register, profile, profile_list

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile_list/', profile_list, name='profile_list'),
]
