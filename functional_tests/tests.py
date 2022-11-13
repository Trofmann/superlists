import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    """
    Тест нового пользователя
    """

    MAX_WAIT = 10

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Завершение"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """
        Ожидание строки в таблице списка
        """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_list_and_retrieve_it_later(self):
        """Тест: можно начать список дел и закончить его позже"""
        # Приложение со списком дел
        self.browser.get(self.live_server_url)

        # Название вкладки
        self.assertIn('To-Do', self.browser.title)

        # Пользователь видит, что заголовок и шапка страницы говорят о списках дел
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('To-Do', header_text)

        # Предложение ввода элемента списка
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # Ввод в текстовом поле 'Купить павлиньи перья'
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает добавить ещё один элемент.
        # Пользователь вводит 'Сделать мушку из павлиньих перьев'
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Страница снова обновляется и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с пояснениями.
        self.fail('Закончить тест')
        # Она посещает этот URL-адрес – ее список по-прежнему там.
