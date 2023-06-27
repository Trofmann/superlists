from unittest.mock import patch, Mock

from django.test import TestCase

from lists.forms import NewListForm


class NewListFormTest(TestCase):
    """
    Тест формы для нового списка
    """

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
            self, mock_list_create_new
    ):
        """
        Тест: save создаёт новый список из POST-данных,
        если пользователь не аутентифицирован
        """
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(
            first_item_text='new item text'
        )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_authenticated(
            self, mock_list_create_new
    ):
        """
        Тест: save создаёт новый список с владельцем,
        если пользователь аутентифицирован
        """
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_list_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user
        )

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_list_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_list_create_new.return_value)
