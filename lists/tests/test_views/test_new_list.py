from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class NewListTest(TestCase):
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

    def test_redirects_after_POST(self):
        """
        Тест: переадресует после post-запроса
        """
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        """
        Тест на не допустимый ввод: отображает домашний шаблон
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """
        Тест: ошибки валидации выводятся на домашней странице
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_template(self):
        """
        Тест на недопустимый ввод: форма передаётся в шаблон
        """
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        """
        Тест: сохраняются недопустимые элементы списка
        """
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
