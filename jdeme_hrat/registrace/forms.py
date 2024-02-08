from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Event
from django.contrib.auth.forms import UserChangeForm



class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):

    ucast_limit = forms.IntegerField(
        required=False,
        widget=forms.Select(choices=[(i, i) for i in range(1, 100)]),  # Možnosti od 1 do 99
        label='Limit účastníků'
    )
    class Meta:
        model = Event
        fields = ['nazev', 'popis', 'hra', 'misto', 'ucast_limit', 'datum_konani', 'image']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_pic')  # Případně přidat další pole