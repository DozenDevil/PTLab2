from django.test import TestCase  # Импортируем TestCase для написания тестов в Django
from shop.models import Product, Purchase  # Импортируем модели Product и Purchase из приложения shop
from datetime import datetime  # Импортируем datetime для работы с датами и временем


# Тестовый класс для модели Product
class ProductTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Создаём два продукта для тестирования
        Product.objects.create(name="book", price="740")  # Создаём продукт "book"
        Product.objects.create(name="pencil", price="50")  # Создаём продукт "pencil"

    # Тестируем правильность типов данных для модели Product
    def test_correctness_types(self):
        # Проверяем, что поле name является строкой
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        # Проверяем, что поле price является целым числом
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        # Проверяем типы данных для другого продукта
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)

    # Тестируем правильность данных для модели Product
    def test_correctness_data(self):
        # Проверяем, что цена для товара "book" равна 740
        self.assertTrue(Product.objects.get(name="book").price == 740)
        # Проверяем, что цена для товара "pencil" равна 50
        self.assertTrue(Product.objects.get(name="pencil").price == 50)


# Тестовый класс для модели Purchase
class PurchaseTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Создаём объект Product для книги
        self.product_book = Product.objects.create(name="book", price="740")
        # Создаём дату и время для теста
        self.datetime = datetime.now()
        # Создаём покупку для теста
        Purchase.objects.create(product=self.product_book,
                                person="Ivanov",  # Имя покупателя
                                address="Svetlaya St.")  # Адрес покупателя

    # Тестируем правильность типов данных для модели Purchase
    def test_correctness_types(self):
        # Проверяем, что поле person является строкой
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).person, str)
        # Проверяем, что поле address является строкой
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).address, str)
        # Проверяем, что поле date является объектом datetime
        self.assertIsInstance(Purchase.objects.get(product=self.product_book).date, datetime)

    # Тестируем правильность данных для модели Purchase
    def test_correctness_data(self):
        # Проверяем, что имя покупателя — "Ivanov"
        self.assertTrue(Purchase.objects.get(product=self.product_book).person == "Ivanov")
        # Проверяем, что адрес покупателя — "Svetlaya St."
        self.assertTrue(Purchase.objects.get(product=self.product_book).address == "Svetlaya St.")
        # Проверяем, что дата покупки совпадает с созданной датой (сравниваем без микросекунд)
        self.assertTrue(Purchase.objects.get(product=self.product_book).date.replace(microsecond=0) == \
                        self.datetime.replace(microsecond=0))
