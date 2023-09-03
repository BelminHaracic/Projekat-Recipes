from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.utils.crypto import get_random_string
from datetime import timedelta

# Create your models here.


class Manager(BaseUserManager):

    def create_superuser(self, email, username, password, name, surname, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, username, password, name, surname, **other_fields)

    def create_user(self, email, username, password, name, surname, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, surname=surname, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(max_length=80, unique=True)

    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    phone = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = Manager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'name', 'surname']

    def __str__(self):
        return self.username


class Sastojak(models.Model):
    naziv = models.CharField(max_length=100)

    voce = 'V'
    povrce = 'P'
    meso = 'M'
    zitarice = 'Z'
    mlijecni_jaja = 'L'
    bilje_zacini = 'B'
    ostali = 'O'
    ulje_mast = 'U'

    tipovi = [
        (voce, 'Voce'),
        (povrce, 'Povrce'),
        (meso, 'Meso'),
        (zitarice, 'Zitarice'),
        (mlijecni_jaja, 'Mlijeko i jaja'),
        (bilje_zacini, 'Biljni i zacini'),
        (ulje_mast, 'Ulje i masti'),
        (ostali, 'Ostali'),
    ]

    tip = models.CharField(max_length=1, choices=tipovi, default=ostali)

    def __str__(self):
        return self.naziv


class Recept(models.Model):
    naziv = models.CharField(max_length=100)
    opis = models.CharField(max_length=500)
    uputa = models.CharField(max_length=1000, blank=True, null=True)
    vrijeme_pripreme = models.TimeField(blank=True, null=True)
    sastojci = models.ManyToManyField(Sastojak, through='SastojakRecept')
    slika = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.naziv


class SastojakRecept(models.Model):
    sastojak = models.ForeignKey(Sastojak, on_delete=models.CASCADE)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
    kolicina = models.IntegerField(default=1)

    gram = 'G'
    broj = 'B'
    komad = 'K'
    kasikica = 'M'
    kasika = 'V'
    soljica = 'S'
    ostali = 'O'

    jedinice = [
        (gram, 'Gram'),
        (broj, 'Broj'),
        (komad, 'Komad'),
        (kasikica, 'Kasikica'),
        (kasika, 'Kasika'),
        (soljica, 'Soljica'),
        (ostali, 'Ostali'),
    ]

    mjerna_jedinica = models.CharField(max_length=1, choices=jedinice, default=broj)

    dodatni_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.recept.naziv + '-' + self.sastojak.naziv


class Komentar(models.Model):
    tekst = models.CharField(max_length=500)
    recept = models.ForeignKey(Recept, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    vrijeme = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + str(self.id)


class Kontakt(models.Model):
    tekst = models.CharField(max_length=500)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    vrijeme = models.DateTimeField(auto_now_add=True)
    email = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.user.name + str(self.id)
