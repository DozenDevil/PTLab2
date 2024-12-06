from django.test import TestCase
from django.urls import reverse
from shop.models import Product


class IndexPageHTMLTest(TestCase):
    def setUp(self):
        # Создаем товары
        self.product1 = Product.objects.create(name="book", price=740)
        self.product2 = Product.objects.create(name="pencil", price=50)

    def test_index_page_renders_correctly(self):
        # Делаем запрос на главную страницу
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что товары отображаются на странице
        self.assertIn("book", response.content.decode('utf-8'))
        self.assertIn("pencil", response.content.decode('utf-8'))
        self.assertIn("740", response.content.decode('utf-8'))
        self.assertIn("50", response.content.decode('utf-8'))

        # Проверяем, что на странице присутствуют правильные ссылки для покупки
        self.assertContains(response, f'href="/buy/{self.product1.id}"')
        self.assertContains(response, f'href="/buy/{self.product2.id}"')


class PurchaseCreateHTMLTest(TestCase):
    def setUp(self):
        # Создаём товар для покупки
        self.product = Product.objects.create(name="book", price=740)

    def test_purchase_create_form_renders_correctly(self):
        # Проверяем, что страница формы покупки доступна
        response = self.client.get(f'/buy/{self.product.id}/')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что форма содержит нужные поля
        self.assertContains(response, 'name="person"')
        self.assertContains(response, 'name="address"')


class PurchaseDoneHTMLTest(TestCase):
    def setUp(self):
        # Создаём товар для покупки
        self.product = Product.objects.create(name="book", price=740)

    def test_purchase_done_renders_correctly(self):
        # Проверяем, что страница подтверждения доступна
        response = self.client.get(f'/purchase_done/?person=Ivanov&address=Svetlaya%20St.')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что страница отображает правильное сообщение
        self.assertContains(response, "Спасибо за покупку, Ivanov!")
        self.assertContains(response, "Ваш заказ будет отправлен на адрес: Svetlaya St.")
