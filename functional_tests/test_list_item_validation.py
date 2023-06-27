from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import FunctionalTest
from .list_page import ListPage


class ItemValidationTest(FunctionalTest):
    """
    Тест валидации элемента списка
    """

    def test_cannot_add_empty_list_items(self) -> None:
        """
        Тест: нельзя добавлять пустые элементы списка
        """
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемента списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element(
            by=By.CSS_SELECTOR, value='#id_text:invalid'
        ))

        # Эдит начинает набирать текст нового элемента и ошибка исчезает
        list_page.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(
            by=By.CSS_SELECTOR, value='#id_text:valid',
        ))

        # И она может отправить его успешно
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(1, 'Buy milk')

        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # И снова браузер не подчиняется
        self.wait_for(lambda: self.browser.find_element(
            by=By.CSS_SELECTOR, value='#id_text:invalid'
        ))

        # И она может его исправить, заполнив поле неким текстом
        list_page.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(
            by=By.CSS_SELECTOR, value='#id_text:valid'
        ))
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table(1, 'Buy milk')
        list_page.wait_for_row_in_list_table(2, 'Make tea')

    def test_cannot_add_duplicate_items(self):
        """
        Тест: нельзя добавлять повторяющиеся элементы
        """
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        list_page.add_list_item('Buy wellies')

        # Она случайно пытается ввести повторяющийся элемент
        input_box = list_page.get_item_input_box()
        input_box.send_keys('Buy wellies')
        input_box.send_keys(Keys.ENTER)

        # Она видит полезное сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    # Не хочу тестировать js
    # def test_error_messages_are_cleared_on_input(self):
    #     """
    #     Тест: сообщения об ошибках очищаются при вводе
    #     """
    #     # Эдит начинает список и вызывает ошибку валидации
    #     text = 'Banter too thick'
    #     self.browser.get(self.live_server_url)
    #     self.get_item_input_box().send_keys(text)
    #     self.get_item_input_box().send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table(f'1: {text}')
    #     self.get_item_input_box().send_keys(text)
    #     self.get_item_input_box().send_keys(Keys.ENTER)
    #
    #     self.wait_for(lambda: self.assertTrue(
    #         self.get_error_element().is_displayed()
    #     ))
    #
    #     # Она начинает набирать в поле ввода, чтобы очистить ошибку
    #     self.get_item_input_box().send_keys('a')
    #
    #     # Она довольна от того, что сообщение об ошибке исчезает
    #     self.wait_for(lambda: self.assertFalse(
    #         self.get_error_element().is_displayed()
    #     ))

    def get_error_element(self):
        """Получить элемент с ошибкой"""
        return self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')
