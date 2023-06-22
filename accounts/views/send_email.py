from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from ..models import Token

CHECK_EMAIL_TEXT = 'Check your email'


def send_login_email(request):
    """Отправить сообщение для входа в систему"""
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + f'?token={str(token.uid)}'
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(request, CHECK_EMAIL_TEXT)
    return redirect('/')
