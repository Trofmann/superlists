import sys

from .models import ListUser, Token


class PasswordlessAuthenticationBackend(object):
    """Серверный процессор беспарольной аутентификации"""

    def authenticate(self, request, uid, **kwargs):
        print(f'uid {uid}', file=sys.stderr)
        token = Token.objects.filter(uid=uid).first()
        if not token:
            print('no token found', file=sys.stderr)
            return None
        print('got token', file=sys.stderr)

        try:
            user = ListUser.objects.get(email=token.email)
            print('got user', file=sys.stderr)
            return user
        except ListUser.DoesNotExist:
            print('new user', file=sys.stderr)
            return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        """Получить пользователя"""
        return ListUser.objects.get(email=email)
