from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR
from lists.models import Item, List
from lists.views import NewListView

User = get_user_model()
factory = RequestFactory()


class NewListIntegratedTest(TestCase):
    """
    Тест нового списка
    """

    def test_can_save_a_POST_request(self):
        """
        Тест: можно сохранить post-запрос
        """
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()  # type: Item

        self.assertEqual(new_item.text, 'A new list item')

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        """
        Тест: недопустимый ввод не сохраняется, но показывает ошибки
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_list_owner_is_saved_if_user_is_authenticated(self):
        """
        Тест: владелец сохраняется, если пользователь аутентифицирован
        """
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'new_item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


class NewListUnitTest(TestCase):
    """Модульный тест нового представления списка"""

    def test_url_exists_at_desired_location(self):
        """
        Тест: такой урл существует
        """
        response = self.client.get('/lists/new')
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        Тест: урл доступен по имени
        """
        response = self.client.get(reverse('new_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        """
        Тест: использует правильный шаблон
        """
        response = self.client.get(reverse('new_list'))
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_form_valid_redirects_to_list_url(self):
        """
        Тест: если форма валидна, то переадресовывается на страницу списка
        """
        user = User.objects.create(email='edith@example.com')
        request = factory.post(
            reverse('new_list'), data={'text': 'new list item'}
        )
        request.user = user

        response = NewListView.as_view()(request)
        response.client = Client()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/1/')
