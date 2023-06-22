from unittest.mock import patch, call

from django.test import TestCase


@patch('accounts.views.login_view.auth')
class LoginViewTest(TestCase):
    """Тест представления входа в систему"""

    def test_redirects_to_home_page(self, mock_auth):
        """
        Тест: переадресуется на домашнюю страницу
        """
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """
        Тест: вызывается authenticate с uid из GET-запроса
        """
        token_uid = 'abcd123'
        self.client.get(f'/accounts/login?token={token_uid}')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid=token_uid)
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        """
        Тест: вызывается auth_login с пользователем, если такой имеется
        """
        token_uid = 'abcd123'
        response = self.client.get(f'/accounts/login?token={token_uid}')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        """
        Тест: не регистрируется в системе, если пользователь не аутентифицирован
        """
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertFalse(mock_auth.login.called)
