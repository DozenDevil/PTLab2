from django.db import models  # Импортируем модуль models для работы с базой данных в Django


# Создаём модель Product для представления товаров в интернет-магазине.
class Product(models.Model):
    # Поле name — текстовое поле для названия товара.
    # max_length=200 ограничивает длину строки до 200 символов.
    name = models.CharField(max_length=200)

    # Поле price — положительное целое число для хранения цены товара.
    # Оно не позволяет значениям быть отрицательными.
    price = models.PositiveIntegerField()

    sold_count = models.PositiveIntegerField(default=0)  # Количество проданных товаров


# Создаём модель Purchase для представления покупок.
class Purchase(models.Model):
    # Поле product — связь с моделью Product (многие к одному).
    # on_delete=models.CASCADE означает, что при удалении товара все связанные покупки будут тоже удалены.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Поле person — текстовое поле для имени покупателя.
    person = models.CharField(max_length=200)

    # Поле address — текстовое поле для адреса доставки.
    address = models.CharField(max_length=200)

    # Поле date — автоматическое добавление текущей даты и времени при создании записи.
    date = models.DateTimeField(auto_now_add=True)
