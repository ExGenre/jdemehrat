
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

         # Cesta na ukládání obrázků k události

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Event(models.Model):
    nazev = models.CharField(max_length=100)
    popis = models.TextField()
    hra = models.TextField()
    misto = models.TextField(default="")
    datum_vytvoreni = models.DateTimeField(auto_now_add=True, null= True)
    datum_konani = models.DateTimeField(null=True)
    image = models.ImageField(default='event_images/defaulteventimage.png', upload_to='event_images/')
    ucast_limit = models.IntegerField(default=0)
    vytvoreno_uzivatelem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class Participation(models.Model):
    uzivatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    udalost = models.ForeignKey(Event, on_delete=models.CASCADE)
    cas = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    udalost = models.ForeignKey(Event, on_delete=models.CASCADE)
    uzivatel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    cas_vytvoreni = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email