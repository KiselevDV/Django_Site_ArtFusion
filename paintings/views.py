from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.views.generic.base import View

from .models import Product, Author
from .forms import ReviewForm


class ProductsView(ListView):
    """Список работ"""
    model = Product
    queryset = Product.objects.filter(draft=False)
    template_name = 'products/products.html'


class ProductDetailView(View):
    """Подробное описание работы"""

    def get(self, request, slug):
        product = Product.objects.get(url=slug)
        return render(request, 'products/product_detail.html', {'product': product})


class NewReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)  # Заполняем форму данными которые пришли из запроса
        product = Product.objects.get(id=pk)  # Получить запсись из объекта
        if form.is_valid():  # Проверяем форму на валидерсть (для сохранения)
            form = form.save(commit=False)  # Отменяем автосохранение (т.к. форма привязывается на определённую работу)
            # до сохранения нужно указать к какой работе привязывать отзыв
            if request.POST.get('parent', None):  # Проверка ключа "parent"
                form.parent_id = request.POST.get('parent')
            form.product = product  # Присвиваем объект форме
            form.save()
        return redirect(product.get_absolute_url())  # Вернуться после выполнения ...


class AuthorView(DeleteView):
    """О авторе"""
    model = Author
    template_name = 'products/author.html'
    slug_field = 'name'  # поле по которуму будем искать (модель: Author, атрибут: name)
