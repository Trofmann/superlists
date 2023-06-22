from django.test import TestCase
from ...models import Token


class TokenModelTest(TestCase):
    """Тест модели маркера"""

    def test_links_user_With_auto_generated_uid(self):
        """
        Тест: соединяет пользователя с автогенерированным uid
        """
        email = 'a@b.com'
        token1 = Token.objects.create(email=email)
        token2 = Token.objects.create(email=email)
        self.assertNotEqual(token1.uid, token2.uid)
