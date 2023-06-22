from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from ..const import EDITH_EMAIL

User = get_user_model()


class AuthenticateTest(TestCase):
    """Тест аутентификации"""

    def test_returns_None_if_no_such_Token(self):
        """
        Тест: возвращается None, есть нет такого маркера
        """
        result = PasswordlessAuthenticationBackend().authenticate(
            self.client.request,
            'no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """
        Тест: возвращается новый пользователь с правильной почтой,
        если маркер существует
        """
        token = Token.objects.create(email=EDITH_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(
            self.client.request,
            token.uid
        )
        new_user = User.objects.get(email=EDITH_EMAIL)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """
        Тест: возвращается существущий пользователь с правильной почтой,
        если маркер существует
        """
        existing_user = User.objects.create(email=EDITH_EMAIL)
        token = Token.objects.create(email=EDITH_EMAIL)
        user = PasswordlessAuthenticationBackend().authenticate(
            self.client.request,
            token.uid
        )
        self.assertEqual(user, existing_user)
