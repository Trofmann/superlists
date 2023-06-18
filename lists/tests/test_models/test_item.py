from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List


class ItemModelTest(TestCase):
    """
    Тест модели элемента списка
    """

    def test_default_text(self):
        """
        Тест заданного по умолчанию текста
        """
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self) -> None:
        """
        Тест: нельзя добавлять пустые элементы списка
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """
        Тест: повторы не допустимы
        """
        text = 'bla'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=text)
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text=text)
            item.full_clean()

    def test_can_save_same_item_to_different_list(self):
        """
        Тест: может сохранить один и тот же элемент в разные списки
        """
        text = 'bla'
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text=text)
        item = Item(list=list2, text=text)
        item.full_clean()  # не должен поднять исключение

    def test_list_ordering(self):
        """
        Тест: упорядочивание списка
        """
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertSequenceEqual(
            Item.objects.all(),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        """
        Тест: строковое представление
        """
        text = 'some text'
        item = Item(text=text)
        self.assertEqual(str(item), text)
