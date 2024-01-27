from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, EventForm
from django.contrib.auth.views import LoginView
from .models import CustomUser, Event, Participation, Comment, UserProfile
from rest_framework import viewsets, status, serializers
from .serializers import EventSerializer, ParticipationSerializer, CommentSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

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


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(vytvoreno_uzivatelem=self.request.user)

# view na vytvoření účasti na události
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
