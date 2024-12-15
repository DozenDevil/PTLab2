from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Purchase


class PurchaseViewTestCase(TestCase):

    def setUp(self):
        # Создаём тестовый продукт
        self.product = Product.objects.create(name="Телевизор", price=50000, sold_count=0)

    # Тест редиректа после успешной покупки
    def test_redirect_after_purchase(self):
        response = self.client.post(reverse('buy', kwargs={'pk': self.product.pk}), {
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1',
            'product': self.product.pk,
        })
        self.assertRedirects(
            response,
            reverse('purchase_done', kwargs={
                'person': 'Иван Иванов',
                'address': 'Москва, ул. Ленина, д. 1'
            })
        )

    # Тест увеличения цены после 10-й покупки
    def test_price_increase_after_tenth_sale(self):
        for _ in range(9):
            Purchase.objects.create(
                product=self.product,
                person="Покупатель",
                address="Адрес"
            )
            self.product.sold_count += 1
            self.product.save()

        # Совершаем 10-ю покупку
        response = self.client.post(reverse('buy', kwargs={'pk': self.product.pk}), {
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1',
            'product': self.product.pk,
        })

        # Проверяем, что произошёл редирект
        self.assertRedirects(
            response,
            reverse('purchase_done', kwargs={
                'person': 'Иван Иванов',
                'address': 'Москва, ул. Ленина, д. 1'
            })
        )

        # Обновляем объект продукта и проверяем, что цена увеличилась
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, round(50000 * 1.15))

    # Тест доступности страницы purchase_done
    def test_purchase_done_page(self):
        response = self.client.get(reverse('purchase_done', kwargs={
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1'
        }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иван Иванов")  # Проверяем, что имя покупателя отображается
        self.assertContains(response, "Москва, ул. Ленина, д. 1")  # Проверяем адрес покупателя

    # Тест создания покупки и увеличения sold_count
    def test_sold_count_increase(self):
        initial_sold_count = self.product.sold_count
        self.client.post(reverse('buy', kwargs={'pk': self.product.pk}), {
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1',
            'product': self.product.pk,
        })

        # Обновляем продукт из базы данных
        self.product.refresh_from_db()
        self.assertEqual(self.product.sold_count, initial_sold_count + 1)

    # Тест создания объекта Purchase
    def test_purchase_creation(self):
        self.client.post(reverse('buy', kwargs={'pk': self.product.pk}), {
            'person': 'Иван Иванов',
            'address': 'Москва, ул. Ленина, д. 1',
            'product': self.product.pk,
        })

        # Проверяем, что объект Purchase создан
        purchase = Purchase.objects.get(product=self.product)
        self.assertEqual(purchase.person, 'Иван Иванов')
        self.assertEqual(purchase.address, 'Москва, ул. Ленина, д. 1')
