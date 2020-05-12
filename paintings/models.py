from django.db import models
from django.urls import reverse
from datetime import date


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Author(models.Model):
    """Фотографы и художники"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Аватарка', upload_to='author/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = 'Фотографы и художники'
        verbose_name_plural = 'Фотографы и художники'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Product(models.Model):
    """Работы"""
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', null=True, blank=True)
    view = models.ImageField('Произведение', upload_to='product/')
    year = models.PositiveSmallIntegerField('Дата создания', default=2020)
    country = models.CharField('Страна', max_length=30, null=True, blank=True)
    author = models.ManyToManyField(Author, verbose_name='Автор', related_name='job_author')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    date_add = models.DateField('Дата размещения', default=date.today)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'


class Collection(models.Model):
    """Все работы из коллекции"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='picture_collection/')
    product = models.ForeignKey(Product, verbose_name='Работа', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Работа из коллекции'
        verbose_name_plural = 'Работы из коллекции'


class OverallRating(models.Model):
    """Значение рейтинга"""
    value = models.PositiveSmallIntegerField('Значение', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(OverallRating, on_delete=models.CASCADE, verbose_name='звезда')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='работа')

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Отзыв"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='От какого коментария',
                               on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name='', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
