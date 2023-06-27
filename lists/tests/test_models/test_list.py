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

    def test_create_new_creates_list_and_first_item(self):
        """
        Тест: create_new создаёт список и первый элемент
        """
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_creates_new_optionally_saves_owner(self):
        """
        Тест: create_new необязательно сохраняет владельца
        """
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        """
        Тест: списки могут иметь владельца
        """
        List(owner=User())  # Не должно поднять исключение

    def test_lists_owner_is_optional(self):
        """
        Тест: владелец списка необязательный
        """
        List().full_clean()  # Не должно поднять исключение

    def test_create_returns_new_list_object(self):
        """
        Тест: create возвращает новый объект списка
        """
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        """
        Тест: имя списка является текстом первого элемента
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')
