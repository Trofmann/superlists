from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, request, uid, **kwargs):
        """Аутентифицировать"""
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=token.email)

    def get_user(self, email):
        """Получить пользователя"""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
