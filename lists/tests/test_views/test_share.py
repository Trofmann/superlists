from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase

from lists.models import List

User = get_user_model()

FRIEND_EMAIL = 'friend@friend.com'


class ShareViewTest(TestCase):
    """
    Тест 'Поделиться списком'
    """

    def post_share(self, list_id: int, email: str = FRIEND_EMAIL) -> HttpResponse:
        return self.client.post(
            f'/lists/{list_id}/share/',
            data={'sharee': email}
        )

    def test_POST_redirects_to_lists_page(self):
        """
        Тест: POST-запрос переадресуется на страницу списка
        """
        user = User.objects.create(email=FRIEND_EMAIL)
        list_ = List.objects.create()
        response = self.post_share(list_.id)
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_user_in_list_shared_with(self):
        """
        Тест: пользователь добавлен в список тех, с кем поделились
        """
        user = User.objects.create(email=FRIEND_EMAIL)
        list_ = List.objects.create()
        self.post_share(list_.id)
        self.assertIn(user, list_.shared_with.all())
