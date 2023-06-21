import sys

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect


def login(request):
    """Регистрация в системе"""
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')
