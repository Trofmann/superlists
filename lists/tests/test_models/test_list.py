from django.contrib.auth import get_user_model
from django.test import TestCase

from ...models import List, Item

User = get_user_model()


class ListModelTest(TestCase):
    """
    Тест модели списка
    """

    def test_get_absolute_url(self):
        """
        Тест: получен абсолютный url
        """
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_lists_can_have_owners(self):
        """
        Тест: списки могут иметь владельцев
        """
        user = User.objects.create(email='a@b.com')
        list_ = List.objects.create(owner=user)
        self.assertIn(list_, user.list_set.all())

    def test_list_owner_is_optional(self):
        """
        Тест: владелец списка является необязательным
        """
        List.objects.create()  # Не должно поднимать исключение

    def test_list_name_is_first_item_text(self):
        """
        Тест: имя списка является текстом первого элемента
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
