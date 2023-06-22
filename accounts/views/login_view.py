from django.shortcuts import redirect
from django.contrib import auth, messages


def login(request):
    """Зарегистрировать вход в систему"""
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
