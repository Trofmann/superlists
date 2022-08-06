from selenium import webdriver
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



# Предложение ввода элемента списка

# Ввод в текстовом поле 'Создать тестовое дело'

# При нажатии на enter страница обновляется
# И содержит: '1: Создать тестовое дело'

# Текстовое поле доступно. Вводим: 'Создать тестовое дело 2'

# Страница обновляется и содержит 2 элемента

# Сайт сгенерировал уникальный url-адрес

# Переход по адресу - список на месте

if __name__ == '__main__':
    pass
