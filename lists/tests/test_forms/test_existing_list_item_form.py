from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import List, Item


class ExistingListItemFormTest(TestCase):
    """Тест формы элемента существующего списка"""

    def test_form_renders_item_text_input(self):
        """
        Тест: форма отображает текстовый ввод элемента
        """
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Тест: валидация формы для пустых элементов
        """
        list_ = List.objects.create()
        data = {'text': ''}
        form = ExistingListItemForm(for_list=list_, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        """
        Тест: валидация формы для повторяющихся элементов
        """
        text = 'no twins!'
        list_ = List.objects.create()
        Item.objects.create(list=list_, text=text)

        form = ExistingListItemForm(for_list=list_, data={'text': text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        """
        Тест: сохранение формы
        """
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
