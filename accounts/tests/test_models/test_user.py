from django.contrib import auth
from django.test import TestCase

from ..const import EDITH_EMAIL

User = auth.get_user_model()


class UserModelTest(TestCase):
    """Тест модели пользователя"""

    def test_user_is_valid_with_email_only(self):
        """
        Тест: пользователь только с почтой допустим
        """
        user = User(email='a@b.com')
        user.full_clean()  # Не должно поднять исключение

    def test_email_is_primary_key(self):
        """
        Тест: адрес электронной почты является первичным ключом
        """
        email = 'a@b.com'
        user = User(email=email)
        self.assertEqual(user.pk, email)

    def test_no_problem_with_auth_login(self):
        """
        Тест: проблем с auth_login нет
        """
        user = User.objects.create(email=EDITH_EMAIL)
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)  # Не должно поднять исключение
