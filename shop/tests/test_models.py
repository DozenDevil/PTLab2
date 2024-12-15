from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Purchase
from datetime import datetime


# Тестовый класс для модели Product
class ProductTestCase(TestCase):

    def setUp(self):
        # Создаём два продукта для тестирования
        self.product_1 = Product.objects.create(name="Телевизор", price=50000)
        self.product_2 = Product.objects.create(name="Ноутбук", price=100000)

    # Тестируем правильность типов данных для модели Product
    def test_correctness_types(self):
        self.assertIsInstance(self.product_1.name, str)  # Поле name — строка
        self.assertIsInstance(self.product_1.price, int)  # Поле price — целое число

    # Тестируем правильность данных для модели Product
    def test_correctness_data(self):
        self.assertEqual(self.product_1.price, 50000)  # Цена для "Телевизор" — 50000
        self.assertEqual(self.product_2.price, 100000)  # Цена для "Ноутбук" — 100000


# Тестовый класс для модели Purchase
class PurchaseTestCase(TestCase):

    def setUp(self):
        # Создаём объект Product для тестирования
        self.product_1 = Product.objects.create(name="Телевизор", price=50000)
        # Создаём покупку для теста
        self.purchase = Purchase.objects.create(
            product=self.product_1,
            person="Иван Иванов",
            address="Москва, ул. Ленина, д. 1"
        )
        # Сохраняем дату и время для сравнения
        self.datetime = self.purchase.date

    # Тестируем правильность типов данных для модели Purchase
    def test_correctness_types(self):
        self.assertIsInstance(self.purchase.person, str)  # Поле person — строка
        self.assertIsInstance(self.purchase.address, str)  # Поле address — строка
        self.assertIsInstance(self.purchase.date, datetime)  # Поле date — datetime

    # Тестируем правильность данных для модели Purchase
    def test_correctness_data(self):
        self.assertEqual(self.purchase.person, "Иван Иванов")  # Имя покупателя
        self.assertEqual(self.purchase.address, "Москва, ул. Ленина, д. 1")  # Адрес покупателя
        self.assertEqual(
            self.purchase.date.replace(microsecond=0),
            self.datetime.replace(microsecond=0)
        )  # Дата покупки

    # Тесты для редиректа после покупки
    def test_redirect_after_purchase(self):
        response = self.client.post(reverse('buy', kwargs={'pk': self.product_1.pk}), {
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1',
            'product': self.product_1.pk,
        })
        self.assertRedirects(
            response,
            reverse('purchase_done', kwargs={
                'person': 'Иван Иванов',
                'address': 'Москва, ул. Ленина, д. 1'
            })
        )

    # Тест корректности данных на странице purchase_done
    def test_purchase_done_page(self):
        response = self.client.get(reverse('purchase_done', kwargs={
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1'
        }))
        self.assertEqual(response.status_code, 200)  # Статус ответа 200
        self.assertContains(response, "Иван Иванов")  # Имя покупателя на странице
        self.assertContains(response, "Москва, ул. Ленина, д. 1")  # Адрес покупателя
