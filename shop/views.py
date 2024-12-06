from django.shortcuts import render, redirect  # Импортируем redirect для перенаправления
from django.http import HttpResponse  # Для отправки текстовых сообщений
from django.views.generic.edit import CreateView  # Для создания форм
from django.views.generic import TemplateView

from .models import Product, Purchase  # Импортируем модели Product и Purchase из текущего приложения


# Функциональное представление для главной страницы
def index(request):
    # Получаем все товары из базы данных
    products = Product.objects.all()

    # Создаём контекст (данные), которые будут переданы в HTML-шаблон
    context = {'products': products}

    # Рендерим шаблон 'shop/index.html' с переданным контекстом
    return render(request, 'shop/index.html', context)


# Класс-представление для создания покупки
class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()  # Сохраняем покупку
        # После сохранения формы, перенаправляем на страницу подтверждения покупки
        return redirect('purchase_done', person=self.object.person, address=self.object.address)


class PurchaseDone(TemplateView):
    template_name = 'shop/purchase_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = self.kwargs.get('person')
        context['address'] = self.kwargs.get('address')
        return context
