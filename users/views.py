from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите в аккаунт.')
            return redirect('login')  # Исправлено для соответствия пространству имён
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, исправьте ошибки.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Вход пользователя
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('home')  # Перенаправление на домашнюю страницу
        else:
            messages.error(request, 'Ошибка при входе. Проверьте свои данные.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')
