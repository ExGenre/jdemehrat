from django.urls import path, include
from .views import register, profile, profile_list, events, create_event, EventViewSet, user_login
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile_list/', profile_list, name='profile_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_login/', user_login, name='user_login'),
    path('login/', user_login, name='login'),
    path('events/', events, name='events'),
    path('create_event/', create_event, name='create_event'),
    path('api/', include(router.urls))
]
