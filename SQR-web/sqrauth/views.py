from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserAuthForm
import pyotp
from django.contrib.auth.decorators import login_required
from qruser.models import User
from django.http import HttpResponseRedirect

def register(request):
    """
    Регистрация
    """
    if request.user.is_authenticated(): #Если пользоватлеь уже авторизован, то перенаправляем на гл. страницу
        return redirect('index')
    if request.method == 'POST': #Если метод не POST, то создаём пустые формы, иначе начинаем создание аккаунта
        form = UserRegisterForm(request.POST) #Берём информацию из формы
        if form.is_valid():
            username = form.cleaned_data['username'] #Берём логин пользовтаеля
            password = form.cleaned_data['password'] #Берём пароль пользовтаеля
            repass = form.cleaned_data['repass']
            email = form.cleaned_data['email'] #Берём почту пользовтаеля
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if password == repass:
                user = User.objects.create_user(username, email, password)

                user.secret_word = pyotp.random_base32();

                sch = form.cleaned_data['school']
                sc = None
                if sch == '1':
                    sc = 'МБОУ СОШ №45'
                elif sch == '2':
                    sc = 'МБОУ лицей №4'
                user.school_name = sc

                kl = form.cleaned_data['klass']
                if len(kl) == 3:
                    klass = kl[0]
                else:
                    klass = kl[:2]
                litera = kl[-1]

                user.school_klass = klass
                user.school_klass_litera = litera
                user.first_name = first_name
                user.last_name = last_name
                user.set_password(password) #Шифруем пароль пользователя
                user.save() #Отправляем пользователя в БД

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def authentication(request):
    """
    Вход в аккаунт
    """
    if request.user.is_authenticated(): #Если пользоватлеь уже авторизован, то перенаправляем на гл. страницу
        return redirect('index')
    if request.method == 'POST':
        form = UserAuthForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return  redirect('index')
    else:
        form = UserAuthForm()

    return render(request, 'auth.html', {'form': form})

def log_out(request):
    """
    Выход из аккаунта
    """
    logout(request)
    return redirect('index')
