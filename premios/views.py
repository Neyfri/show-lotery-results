from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'GET':
        contenxt = {'form' : UserCreationForm }
        return render(request, 'register.html', contenxt)
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registrar nuevo usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('mainpage')
            except IntegrityError:
                contenxt = {'form' : UserCreationForm, 'error' : 'Este usuario ya existe.'}
                return render(request, 'register.html', contenxt)
        contenxt = {'form' : UserCreationForm, 'error' : 'Las contrasenas no coinciden.'}
        return render(request, 'register.html', contenxt)

def indexPage(request):
    page = requests.get('https://www.conectate.com.do/loterias/')
    soup = BeautifulSoup(page.content, 'html.parser')
    #Premios
    bolos = soup.find_all('span', class_='score')
    numeros = list()
    for i in bolos:
        numeros.append(i.text.strip())
    lNacional = numeros[8:11]
    qLeidsa = numeros[39:42]
    qReal = numeros[50:53]
    qLoteka = numeros[63:66]
    return render(request, 'index.html', {'r1':lNacional, 'r2':qLeidsa, 'r3':qReal, 'r4':qLoteka})

def signin(request):
    if request.method == 'GET':
        context = { 'form' : AuthenticationForm}
        return render(request, 'signin.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password= request.POST['password'])
        if user is None:
            context = { 'form' : AuthenticationForm, 'error': 'Usuario O Contreña no Validos'}
            return render(request, 'signin.html', context)
        else:
            login(request, user)
            return redirect('/mainpage')
@login_required
def mainPage(request):
    username = get_user(request).username
    return render(request, 'mainpage.html', {'cuser':username})
@login_required
def signout(request):
    logout(request)
    return redirect('/')