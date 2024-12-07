from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase
from datetime import datetime


# Тестовый класс для представления PurchaseCreate
class PurchaseCreateTestCase(TestCase):

    # Метод setUp выполняется перед каждым тестом и создаёт необходимые объекты
    def setUp(self):
        # Создаём тестовый продукт
        self.product = Product.objects.create(name="Телевизор", price=50000)

        # Инициализируем клиент для отправки запросов в тестах
        self.client = Client()

    # Тестируем создание покупки через форму
    def test_purchase_create_view(self):
        # Отправляем POST-запрос с данными формы на создание покупки
        response = self.client.post(reverse('buy', args=[self.product.pk]), {
            'product': self.product.pk,
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1'
        })

        print(f"Redirecting to purchase_done with {self.object.person}, {self.object.address}")

        # Проверяем, что редирект происходит на страницу подтверждения покупки
        self.assertRedirects(response, reverse('purchase_done', kwargs={'person': 'Иван Иванов', 'address': 'Москва, ул. Ленина, д. 1'}))

        # Проверяем, что покупка была успешно создана в базе данных
        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.first()
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.person, 'Иван Иванов')
        self.assertEqual(purchase.address, 'Москва, ул. Ленина, д. 1')

    # Тестируем, что количество проданных товаров увеличивается
    def test_sold_count_increases(self):
        initial_sold_count = self.product.sold_count
        self.client.post(reverse('buy', args=[self.product.pk]), {
            'product': self.product.pk,
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1'
        })
        self.product.refresh_from_db()  # Обновляем объект продукта из базы данных
        self.assertEqual(self.product.sold_count, initial_sold_count + 1)

    # Тестируем, что цена увеличивается после каждых 10 продаж
    def test_price_increase_after_tenth_sale(self):
        self.product.sold_count = 9
        self.product.save()
        self.client.post(reverse('buy', args=[self.product.pk]), {
            'product': self.product.pk,
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1'
        })
        self.product.refresh_from_db()  # Обновляем объект продукта из базы данных

        # Ожидаемая цена с увеличением на 15%
        expected_price = int(50000 * 1.15)  # Приводим к целому числу, отбросив дробную часть

        # Проверяем, что цена товара после увеличения равна ожидаемой целой цене
        self.assertEqual(self.product.price, expected_price)
