import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    """
    Тест нового пользователя
    """

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Chrome()

    def tearDown(self):
        """Завершение"""
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        """Тест: можно начать список дел и закончить его позже"""
        # Приложение со списком дел
        self.browser.get('http://127.0.0.1:8000/')

        # Название вкладки
        self.assertIn('To-Do', self.browser.title)

        # Пользователь видит, что заголовок и шапка страницы говорят о списках дел
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('To-Do', header_text)

        # Предложение ввода элемента списка
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # Ввод в текстовом поле 'Создать тестовое дело'
        input_box.send_keys('Создать тестовое дело')

        # При нажатии на enter страница обновляется
        # И содержит: '1: Создать тестовое дело'
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertTrue(
            any(row.text == '1: Создать тестовое дело' for row in rows)
        )

        # Текстовое поле доступно. Вводим: 'Создать тестовое дело 2'
        self.fail('Закончить тест')


# Страница обновляется и содержит 2 элемента

# Сайт сгенерировал уникальный url-адрес

# Переход по адресу - список на месте
if __name__ == '__main__':
    pass
