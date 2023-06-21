from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def logout(request):
    """Выход из системы"""
    auth_logout(request)
    return redirect('/')
