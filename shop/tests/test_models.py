from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime


# Тестовый класс для модели Product
class ProductTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Создаём два продукта для тестирования
        self.product_1 = Product.objects.create(name="Телевизор", price=50000)
        self.product_2 = Product.objects.create(name="Ноутбук", price=100000)

    # Тестируем правильность типов данных для модели Product
    def test_correctness_types(self):
        # Проверяем, что поле name является строкой
        self.assertIsInstance(self.product_1.name, str)
        # Проверяем, что поле price является целым числом
        self.assertIsInstance(self.product_1.price, int)

    # Тестируем правильность данных для модели Product
    def test_correctness_data(self):
        # Проверяем, что цена для товара "Телевизор" равна 50000
        self.assertEqual(self.product_1.price, 50000)
        # Проверяем, что цена для товара "Ноутбук" равна 100000
        self.assertEqual(self.product_2.price, 100000)

    # Тестируем метод увеличения цены на 15%
    def test_increase_price(self):
        # Увеличиваем цену первого продукта
        self.product_1.increase_price()
        # Проверяем, что цена увеличилась на 15%
        self.assertEqual(self.product_1.price, 50000 * 1.15)

        # Увеличиваем цену второго продукта
        self.product_2.increase_price()
        # Проверяем, что цена второго продукта увеличилась на 15%
        self.assertEqual(self.product_2.price, 100000 * 1.15)


# Тестовый класс для модели Purchase
class PurchaseTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Создаём объект Product для тестирования
        self.product_1 = Product.objects.create(name="Телевизор", price=50000)
        # Создаём покупку для теста
        self.purchase = Purchase.objects.create(
            product=self.product_1,
            person="Иван Иванов",  # Имя покупателя
            address="Москва, ул. Ленина, д. 1"  # Адрес покупателя
        )
        # Дата и время для теста
        self.datetime = self.purchase.date

    # Тестируем правильность типов данных для модели Purchase
    def test_correctness_types(self):
        # Проверяем, что поле person является строкой
        self.assertIsInstance(self.purchase.person, str)
        # Проверяем, что поле address является строкой
        self.assertIsInstance(self.purchase.address, str)
        # Проверяем, что поле date является объектом datetime
        self.assertIsInstance(self.purchase.date, datetime)

    # Тестируем правильность данных для модели Purchase
    def test_correctness_data(self):
        # Проверяем, что имя покупателя — "Иван Иванов"
        self.assertEqual(self.purchase.person, "Иван Иванов")
        # Проверяем, что адрес покупателя — "Москва, ул. Ленина, д. 1"
        self.assertEqual(self.purchase.address, "Москва, ул. Ленина, д. 1")
        # Проверяем, что дата покупки совпадает с созданной датой
        self.assertEqual(self.purchase.date.replace(microsecond=0), self.datetime.replace(microsecond=0))