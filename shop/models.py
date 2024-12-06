from django.db import models  # Импортируем модуль models для работы с базой данных в Django


# Создаём модель Product для представления товаров в интернет-магазине.
class Product(models.Model):
    # Поле name — текстовое поле для названия товара.
    # max_length=200 ограничивает длину строки до 200 символов.
    name = models.CharField(max_length=200)

    # Поле price — положительное целое число для хранения цены товара.
    # Оно не позволяет значениям быть отрицательными.
    price = models.PositiveIntegerField()

    # Метод __str__ определяет строковое представление объекта модели.
    # Например, в админке или при выводе в консоль вместо <Product: Product object (1)>
    # объект будет отображаться как "Название товара - цена".
    # Удобно для отладки и админки, но в данном случае метод закомментирован.
    # def __str__(self):
    #     return f"{self.name} - {self.price} ₽"


# Создаём модель Purchase для представления покупок.
class Purchase(models.Model):
    # Поле product — связь с моделью Product (многие ко одному).
    # on_delete=models.CASCADE означает, что при удалении товара все связанные покупки будут тоже удалены.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Поле person — текстовое поле для имени покупателя.
    person = models.CharField(max_length=200)

    # Поле address — текстовое поле для адреса доставки.
    address = models.CharField(max_length=200)

    # Поле date — автоматическое добавление текущей даты и времени при создании записи.
    date = models.DateTimeField(auto_now_add=True)

    # Метод __str__ определяет строковое представление объекта модели.
    # Например, в админке или при выводе в консоль вместо <Purchase: Purchase object (1)>
    # объект будет отображаться как "Purchase by имя покупателя on дата".
    # Удобно для отладки и админки, но в данном случае метод закомментирован.
    # def __str__(self):
    #     return f"Purchase by {self.person} on {self.date.strftime('%Y-%m-%d')}"
