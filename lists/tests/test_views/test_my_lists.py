from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

EMAIL = 'a@b.com'


class MyListsTest(TestCase):
    """Тест 'Мои списки'"""

    def test_my_lists_url_renders_my_lists_template(self):
        """
        Тест: url-aадрес для 'моих списков' отображает соответствующий им шаблон
        """
        email = EMAIL
        User.objects.create(email=email)
        response = self.client.get(f'/lists/users/{email}/')
        self.assertTemplateUsed(response, 'lists/my_lists.html')

    def test_passes_correct_owner_to_template(self):
        """
        Тест: передаётся правильный владелец в шаблон
        """
        User.objects.create(email='wrong@owner.com')
        right_email = EMAIL
        correct_user = User.objects.create(email=right_email)
        response = self.client.get(f'/lists/users/{right_email}/')
        self.assertEqual(response.context['owner'], correct_user)
