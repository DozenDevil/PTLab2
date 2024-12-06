from django.test import TestCase, \
    Client  # Импортируем TestCase для написания тестов и Client для эмуляции HTTP-запросов
from shop.views import PurchaseCreate  # Импортируем класс PurchaseCreate из views для тестирования


# Тестовый класс для проверки доступности веб-страниц
class PurchaseCreateTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Инициализируем клиент для отправки запросов в тестах
        self.client = Client()

    # Тестируем доступность главной страницы
    def test_webpage_accessibility(self):
        # Отправляем GET-запрос на главную страницу сайта
        response = self.client.get('/')

        # Проверяем, что сервер возвращает статус код 200 (ОК)
        self.assertEqual(response.status_code, 200)
