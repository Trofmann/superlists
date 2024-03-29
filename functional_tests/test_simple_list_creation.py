from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .list_page import ListPage


class NewVisitorTest(FunctionalTest):
    """
    Тест нового пользователя
    """

    def test_can_start_a_list_for_one_user(self):
        """
        Тест: можно начать список для одного пользователя
        """
        # Эдит слышала про крутое новое онлайн-приложение со списком
        # Приложение со списком дел
        self.browser.get(self.live_server_url)

        list_page = ListPage(self)

        # Название вкладки
        self.assertIn('To-Do', list_page.get_title())

        # Пользователь видит, что заголовок и шапка страницы говорят о списках дел
        header_text = list_page.get_header().text
        self.assertIn('To-Do', header_text)

        # Предложение ввода элемента списка
        input_box = list_page.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Ввод в текстовом поле 'Купить павлиньи перья'
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(1, 'Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает добавить ещё один элемент.
        # Пользователь вводит 'Сделать мушку из павлиньих перьев'
        input_box = list_page.get_item_input_box()
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(2, 'Сделать мушку из павлиньих перьев')

        # Страница снова обновляется и теперь показывает оба элемента списка
        list_page.wait_for_row_in_list_table(1, 'Купить павлиньи перья')
        list_page.wait_for_row_in_list_table(2, 'Сделать мушку из павлиньих перьев')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """
        Тест: многочисленные пользователи могут начать списки дел по разным url
        """
        # Эдит начинает свой список
        self.browser.get(self.live_server_url)

        list_page = ListPage(self)

        input_box = list_page.get_item_input_box()
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(1, 'Купить павлиньи перья')

        # Она замечает, что её список имеет уникальный URL-адрес
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Теперь новый пользователь, Фрэнсис, приходит на сайт.
        # Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        # информация от Эдит не прошла через данные cookie и др.
        self.browser.quit()
        self.browser = self.USING_BROWSER()

        # Фрэнсис посещает домашнюю страницу. Нет никаких признаков списка Эдит
        self.browser.get(self.live_server_url)
        page_text = list_page.get_body().text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        # Фрэнсис начинает новый список, вводя новый элемент.
        input_box = list_page.get_item_input_box()
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(1, 'Купить молоко')

        # Фрэнсис получает уникальный URL-адрес
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Опять-таки, нет ни следа от списка Эдит
        page_text = list_page.get_body().text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)
