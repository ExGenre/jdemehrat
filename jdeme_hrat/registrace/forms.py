from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Upravíme pole username, aby mělo stejný label jako email
        self.fields['username'].label = 'Email'

    def clean(self):
        # Překopírovat hodnotu z pole email do pole username, pokud existuje
        if 'username' in self.cleaned_data:
            self.cleaned_data['username'] = self.cleaned_data['username']
        return super().clean()