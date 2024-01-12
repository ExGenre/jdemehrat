from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Event



class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['nazev', 'popis', 'hra', 'misto', 'datum_konani']