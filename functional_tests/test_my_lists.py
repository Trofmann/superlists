from selenium.webdriver.common.by import By

from .base import FunctionalTest

EDITH_EMAIL = 'edith@example.com'


class MyListTest(FunctionalTest):
    """Тест приложение 'Мои списки'"""

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """
        Тест: списки зарегистрированных пользователей
        сохраняются как 'мои списки'
        """
        email = EDITH_EMAIL
        self.create_pre_authenticated_session(email)

        # Эдит является зарегистрированным пользователем
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # Она замечает ссылку на 'Мои списки' в первый раз
        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()

        # Она видит, что её список находится там и он назван
        # на основе первого элемента списка
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value='Reticulate splines')
        )
        self.browser.find_element(by=By.LINK_TEXT, value='Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает начать ещё один список, чтобы только убедиться
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Под заголовком 'Мои списки' появляется её новый список
        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value='Click cows')
        )
        self.browser.find_element(by=By.LINK_TEXT, value='Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция 'Мои списки' исчезает
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(by=By.LINK_TEXT, value='My lists'), []
            )
        )
