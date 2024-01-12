from django.urls import path
from . import views
from .views import logout_and_redirect
from .views import index

urlpatterns = [
    path('', views.index, name='index'),
    path('logout-and-redirect/', logout_and_redirect, name='logout_and_redirect'),
    path('index/', index, name='index')
    # ...
    # Další URL patterns...
]
