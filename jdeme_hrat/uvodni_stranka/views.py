from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required # kontroluje jestli je uživatel přihlášen
def index(request):
    return render(request, 'uvodni_stranka/index.html')


def logout_and_redirect(request): # odhlášení a přesměrování na register
    logout(request)
    return redirect('register')




