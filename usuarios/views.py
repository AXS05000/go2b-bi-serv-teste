from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import CustomUsuario


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Verifique a contagem de tentativas de login do usuário
        attempt_count = cache.get(f'login-attempts-{username}', 0)
        block_time = cache.get(f'block-time-{username}')

        # Verifica se o usuário está bloqueado
        if block_time and block_time > timezone.now():
            messages.error(request, 'Seu acesso está bloqueado por 24 horas devido a várias tentativas de login falhas.')
            return render(request, 'registration/login.html', {'error': messages.get_messages(request)})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Se a autenticação for bem-sucedida, redefina a contagem de tentativas de login t@gmail.com / Mala@12345
            cache.set(f'login-attempts-{username}', 0)
            cache.set(f'block-time-{username}', None)
            login(request, user)
            return redirect('index')
        else:
            # Incrementar a contagem de tentativas de login
            cache.set(f'login-attempts-{username}', attempt_count + 1)

            # Se o usuário falhou em fazer login 5 vezes, bloqueie-o por 24 horas
            if attempt_count + 1 >= 5:
                block_until = timezone.now() + timedelta(hours=24)
                cache.set(f'block-time-{username}', block_until)
                messages.error(request, 'Seu acesso está bloqueado por 24 horas devido a várias tentativas de login falhas.')
            else:
                messages.error(request, 'Email ou senha incorretos')

            return render(request, 'registration/login.html', {'error': messages.get_messages(request)})

    return render(request, 'registration/login.html', {'error': messages.get_messages(request)})




@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


def handler404(request, exception):
    return render(request, 'page/404.html', status=404)
