from django.test import TestCase


class SmokeTest(TestCase):
    """Тестовый тест"""

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
