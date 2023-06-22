from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from ..const import EDITH_EMAIL

User = get_user_model()


class GetUserTest(TestCase):
    """Тест получение пользователя"""

    def test_gets_user_by_email(self):
        """
        Тест: получает пользователя по адресу электронной почты
        """
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email=EDITH_EMAIL)
        found_user = PasswordlessAuthenticationBackend().get_user(EDITH_EMAIL)
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """
        Тест: возвращается None, если нет пользователя с таким адресом электронной почты
        """
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(EDITH_EMAIL)
        )
