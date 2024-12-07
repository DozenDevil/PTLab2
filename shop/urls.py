from django.urls import path  # Импортируем функцию path для создания маршрутов
from . import views  # Импортируем модуль views из текущего приложения


# Определяем список маршрутов для приложения
urlpatterns = [
    # Главная страница:
    # Маршрут '' (пустая строка) соответствует корневому URL приложения.
    # Он вызывает функцию `index` из модуля views и задаёт имя маршрута 'index'.
    path('', views.index, name='index'),

    # Страница для покупки товара:
    # Маршрут 'buy/<int:product_id>/' принимает целочисленный параметр product_id.
    # Он вызывает класс PurchaseCreate из views (используется CBV — Class-Based View).
    # Имя маршрута 'buy' позволяет удобно ссылаться на этот маршрут в шаблонах.
    path('buy/<int:pk>/', views.PurchaseCreate.as_view(), name='buy'),

    # Маршрут для страницы подтверждения
    path('purchase_done/<str:person>/<str:address>/', views.PurchaseDone.as_view(), name='purchase_done'),
]
