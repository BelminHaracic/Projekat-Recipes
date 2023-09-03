from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *
import random

# Create your views here.


def index(request):
    recepti = Recept.objects.all()
    sastojci = Sastojak.objects.all()
    popularni_recepti = random.sample(list(recepti), 4)

    context = {
        'user': request.user,
        'recepti': recepti,
        'sastojci': sastojci,
        'popularni_recepti': popularni_recepti
    }
    return render(request, 'index.html', context)


# ustimaj da radi fino za kad imaju stranice a ne sa modalima
def registration(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        surname = request.POST['surname']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect('registration')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect('registration')

            else:
                user = User.objects.create_user(username=username, email=email, password=password, name=name,
                                                surname=surname)
                user.is_active = True
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password not the same")
            return redirect('registration')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":

        password = request.POST['password']
        email = request.POST['email']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            messages.info(request, "Wrong credentials")
            return render(request, 'index.html')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')


def delete_acc(request):
    User = get_user_model()

    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id=id)
        user.delete()
        auth.logout(request)
        return render(request, 'index.html')

    else:
        return render(request, 'index.html')


def preporuka_recepta(request):
    selected_items = []
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
    else:
        sastojci = Sastojak.objects.all()

    odabrani_sastojci = Sastojak.objects.filter(id__in=selected_items)
    recepti = Recept.objects.all()
    sastojci = Sastojak.objects.all()
    preporuceni_recepti = []

    for recept in recepti:
        if all(elementi in odabrani_sastojci for elementi in recept.sastojci.all()):
            preporuceni_recepti.append(recept)

    context = {
        'sastojci': sastojci,
        'preporuceni_recepti': preporuceni_recepti,
    }

    return render(request, 'preporuka_recepta.html', context)


def pretraga_recepata(request):
    query = request.GET.get('q')

    if query:
        recepti = Recept.objects.filter(naziv__icontains=query) | Recept.objects.filter(opis__icontains=query)
    else:
        recepti = Recept.objects.all()

    context = {
        'recepti': recepti,
        'query': query
    }
    return render(request, 'pretraga_recepata.html', context)


def kontakt(request):
    if request.method == 'POST':
        poruka = request.POST['poruka']
        email = request.POST['email']

        user = request.user
        kontaktiranje = Kontakt.objects.create(tekst=poruka, user=user, email=email)
        kontaktiranje.save()

    return render(request, 'kontakt.html')


def autori(request):
    return render(request, 'autori.html')


def prikazi_recept(request, recept_id):
    recept = Recept.objects.get(id=recept_id)

    if request.method == 'POST':
        komentar = request.POST['komentar']
        novi_komentar = Komentar.objects.create(tekst=komentar, user=request.user, recept=recept)
        novi_komentar.save()

        return redirect('prikazi_recept', recept_id=recept_id)

    komentari = Komentar.objects.filter(recept_id=recept_id)
    context = {
        'recept': recept,
        'komentari': komentari,
    }

    return render(request, 'prikazi_recept.html', context)


def izbrisi_komentar(request, komentar_id):
    comment = get_object_or_404(Komentar, id=komentar_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        comment.delete()

    # Redirect to the same page after deleting the comment
    return redirect('prikazi_recept', recept_id=comment.recept.id)


def edit_komentar(request, komentar_id):
    komentar = get_object_or_404(Komentar, id=komentar_id)

    if request.method == 'POST':
        new_text = request.POST['new_text']
        komentar.tekst = new_text
        komentar.save()

        # Redirect to the same page after editing the comment
        return redirect('prikazi_recept', recept_id=komentar.recept.id)

    context = {
        'comment': komentar,
    }

    return render(request, 'edit_comment.html', context)
