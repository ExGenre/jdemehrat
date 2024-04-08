from django.urls import path, include
from .views import logout_and_redirect, index, register, profile, profile_list, events, create_event, EventViewSet, user_login, event_detail, \
    ParticipationViewSet, CommentViewSet, UserProfileViewSet,  delete_event, edit_event, user_profile, edit_profile, change_password,\
    cancel_participation, todo
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participations', ParticipationViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'userprofile', UserProfileViewSet)

urlpatterns = [
    path('logout-and-redirect/', logout_and_redirect, name='logout_and_redirect'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('profile/<int:user_id>/', user_profile, name='user_profile'),
    path('profile/', profile, name='profile'),
    path('profile_list/', profile_list, name='profile_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user_login/', user_login, name='user_login'),
    path('login/', user_login, name='login'),
    path('events/', events, name='events'),
    path('create_event/', create_event, name='create_event'),
    path('api/', include(router.urls)),
    path('event-detail/<int:event_id>/', event_detail, name='event-detail'),
    path('api/events/<int:event_id>/delete/', delete_event, name='delete_event'),
    path('edit_event/<int:event_id>/', edit_event, name='edit_event'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('password_change/', change_password, name='change_password'),
    path('cancel-participation/<int:event_id>/', cancel_participation, name='cancel_participation'),
    path('todo/', todo, name='todo'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
