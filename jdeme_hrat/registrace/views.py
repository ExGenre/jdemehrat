from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, EventForm, CustomUserChangeForm
from django.contrib.auth.views import LoginView
from .models import CustomUser, Event, Participation, Comment, UserProfile
from rest_framework import viewsets, status, serializers
from .serializers import EventSerializer, ParticipationSerializer, CommentSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# kontroluje jestli je uživatel přihlášen
def index(request):
    return render(request, 'events.html')


def logout_and_redirect(request): # odhlášení a přesměrování na register
    logout(request)
    return redirect('register')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def profile_list(request):
    users = CustomUser.objects.all()  # Získá všechny uživatele z databáze
    return render(request, 'profile_list.html', {'users': users})


@login_required
def profile(request):
    return render(request, 'profile.html')

def user_profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'user_profile.html', {'profile_user': user})

@login_required
def events(request):
    return render(request, 'events.html')



class CustomLoginView(LoginView):
    def form_valid(self, form):
        print("Přihlašovací formulář je platný.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Přihlašovací formulář je neplatný.")
        return super().form_invalid(form)


@login_required
def create_event(request):
    ucast_limit_choices = [i for i in range(1, 100)]  # Vytvoří seznam od 1 do 99

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.vytvoril = request.user
            event.save()
            return redirect('events')  # Presmerovani na seznam udalosti
    else:
        form = EventForm()

    context = {
        'form': form,
        'ucast_limit_choices': ucast_limit_choices,
    }
    return render(request, 'create_event.html', context)



def event_detail(request, event_id):
    # Získání události podle ID nebo vrácení 404 chyby, pokud neexistuje
    event = get_object_or_404(Event, id=event_id)

    # Kontext pro šablonu
    context = {
        'event': event,
    }

    # Render šablony s kontextem
    return render(request, 'event-detail.html', context)

# View na zakládání a úpravu událostí
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    # Uložení uživatele zakládajícího událost
    def perform_create(self, serializer):
        serializer.save(vytvoreno_uzivatelem=self.request.user)

    # Úprava události a ověření uživatele
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.vytvoreno_uzivatelem != request.user:
            raise PermissionDenied(detail="Nemáte oprávnění upravit tuto událost.")
        return super().update(request, *args, **kwargs)

# view na uživatelskou účast v události
class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['udalost']
        user = self.request.user

        # Kontrola, zda uživatel již není přihlášen k této události
        if Participation.objects.filter(uzivatel=user, udalost=event).exists():
            raise ValidationError({'detail': 'Uživatel je již přihlášen k této události.'})
        # Kontrola, zda je dosažen maximální limit účastníků
        if event.ucast_limit > 0 and event.participation_set.count() >= event.ucast_limit:
            raise ValidationError({'detail': 'Limit účastníků této události byl dosažen.'})

        serializer.save(uzivatel=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@api_view(['DELETE'])
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if event.vytvoreno_uzivatelem != request.user:
        return Response({'error': 'Nemáte oprávnění tuto událost smazat.'},
                        status=status.HTTP_403_FORBIDDEN)

    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Úprava události, ověření uživatele, POST na databázi
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, vytvoreno_uzivatelem=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserChangeForm

# Úprava profilu
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)  # Přidání request.FILES
        if form.is_valid():
            form.save()
            return redirect('profile')  # Přesměrování na profil po úspěšné úpravě
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Důležité pro udržení uživatele přihlášeného
            messages.success(request, 'Vaše heslo bylo úspěšně změněno.')
            return redirect('profile')
        else:
            messages.error(request, 'Prosím opravte chybu níže.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def cancel_participation(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    Participation.objects.filter(udalost=event, uzivatel=request.user).delete()
    # Přesměrujte uživatele zpět na stránku s detaily události nebo jinam
    return redirect('event-detail', event_id=event_id)