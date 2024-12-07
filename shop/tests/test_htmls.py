from django.test import TestCase
from django.urls import reverse
from shop.models import Product


class IndexPageHTMLTest(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name='Laptop', price=50000, sold_count=3)
        self.product2 = Product.objects.create(name='Smartphone', price=30000, sold_count=7)

    def test_index_page_renders_correctly(self):
        # Запрос к главной странице
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        # Проверяем, что название товаров, их цена и количество проданных отображаются
        html_content = response.content.decode('utf-8')
        self.assertIn(self.product1.name, html_content)
        self.assertIn(str(self.product1.price), html_content)
        self.assertIn(str(self.product1.sold_count), html_content)

        self.assertIn(self.product2.name, html_content)
        self.assertIn(str(self.product2.price), html_content)
        self.assertIn(str(self.product2.sold_count), html_content)

        # Проверяем, что ссылки "Купить" корректно отображаются
        self.assertIn(f'/buy/{self.product1.id}', html_content)
        self.assertIn(f'/buy/{self.product2.id}', html_content)


class PurchaseFormTest(TestCase):
    def setUp(self):
        # Создаём тестовый продукт
        self.product = Product.objects.create(
            name='Телевизор', price=50000
        )

    def test_purchase_form_renders_correctly(self):
        # Получаем страницу с формой покупки
        response = self.client.get(reverse('buy', args=[self.product.pk]))

        # Декодируем ответ, чтобы работать с ним как с текстом
        html_content = response.content.decode('utf-8')

        # Проверяем, что страница вернулась с успешным статусом
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице есть текст формы
        self.assertIn('<form method="post">', html_content)

        # Проверяем, что на странице есть поле ввода для имени покупателя
        self.assertIn('<input type="text" name="person"', html_content)

        # Проверяем, что на странице есть поле ввода для адреса доставки
        self.assertIn('<input type="text" name="address"', html_content)

        # Проверяем, что на странице есть кнопка отправки формы
        self.assertIn('<button type="submit" class="btn btn-primary">Отправить</button>', html_content)


class PurchaseDoneTest(TestCase):
    def setUp(self):
        # Информация о покупателе
        self.person = 'Иван Иванов'
        self.address = 'Москва, ул. Ленина, д. 1'

    def test_purchase_done_renders_correctly(self):
        # Отправляем GET-запрос на страницу подтверждения покупки
        response = self.client.get(reverse('purchase_done', args=[self.person, self.address]))

        # Декодируем ответ, чтобы работать с ним как с текстом
        html_content = response.content.decode('utf-8')

        # Проверяем, что страница вернулась с успешным статусом
        self.assertEqual(response.status_code, 200)

        # Проверяем, что на странице есть сообщение о подтверждении покупки
        self.assertIn('Спасибо за покупку!', html_content)

        # Проверяем, что на странице отображается имя покупателя
        self.assertIn(self.person, html_content)

        # Проверяем, что на странице отображается адрес доставки
        self.assertIn(self.address, html_content)
