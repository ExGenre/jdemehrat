from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm, EventForm
from django.contrib.auth.views import LoginView
from .models import CustomUser, Event, Participation, Comment, UserProfile
from rest_framework import viewsets, status, serializers
from .serializers import EventSerializer, ParticipationSerializer, CommentSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class JoinEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        try:
            event = Event.objects.get(pk=pk)
            # Zde můžete přidat další logiku, např. kontrolu limitu účastníků

            # Vytvoření záznamu Participation
            participation = Participation.objects.create(
                uzivatel=request.user,
                udalost=event
            )
            serializer = ParticipationSerializer(participation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Event.DoesNotExist:
            return Response({'message': 'Událost neexistuje'}, status=status.HTTP_404_NOT_FOUND)


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
    return render(request, 'register.html', {'form': form})


def profile_list(request):
    users = CustomUser.objects.all()  # Získá všechny uživatele z databáze
    return render(request, 'registrace/profile_list.html', {'users': users})


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
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.vytvoril = request.user
            event.save()
            return redirect('events')  # Presmerovani na seznam udalosti
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})



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

class ParticipationViewSet(viewsets.ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        event = serializer.validated_data['udalost']
        user = self.request.user

        # Kontrola, zda uživatel již není přihlášen k této události
        if Participation.objects.filter(uzivatel=user, udalost=event).exists():
            raise serializers.ValidationError('Uživatel je již přihlášen k této události.')

        serializer.save(uzivatel=user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer