from django.contrib import admin
from django.contrib.gis import forms
from django.utils.safestring import mark_safe

from .models import Category, Author, Genre, Product, Collection, OverallRating, Rating, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Category
        model = Author
        model = Genre
        model = Product
        model = Collection
        fields = '__all__'


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class AuthorInline(admin.TabularInline):
    model = Author
    extra = 1


class GenreInline(admin.TabularInline):
    model = Genre
    extra = 1


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1


class CollectionInline(admin.TabularInline):
    model = Collection
    extra = 1
    readonly_fields = ('photo_of_works',)

    def photo_of_works(self, picture):
        return mark_safe(f'<img src={picture.image.url} width="120" height="160"')

    photo_of_works.short_description = 'Работы из коллекции'


class OverallRatingInline(admin.StackedInline):
    model = OverallRating
    extra = 1


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 1


class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('name', 'url', 'id')
    list_display_links = ('name', 'url')
    save_on_top = True
    form = ProductAdminForm
    inlines = [ProductInline]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Авторы"""
    list_display = ('name', 'age', 'show_avatar')
    list_display_links = ('name', 'age')
    list_filter = ('name', 'age')
    search_fields = ('name', 'age')
    readonly_fields = ('show_avatar',)
    form = ProductAdminForm

    def show_avatar(self, picture):
        return mark_safe(f'<img src={picture.image.url} width="60" height="80"')

    show_avatar.short_description = 'Аватарка'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url', 'id')
    list_display_links = ('name', 'url')
    search_fields = ('name',)
    form = ProductAdminForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Работы"""
    list_display = ('title', 'year', 'country', 'category', 'url', 'date_add', 'draft')
    list_display_links = ('title', 'year', 'country', 'category')
    list_filter = ('year', 'country', 'category')
    search_fields = ('title', 'year', 'category__name')
    list_editable = ('draft',)
    readonly_fields = ('cover',)
    save_on_top = True
    save_as = True
    save_as_continue = True
    actions = ['publish', 'unpublish']
    fieldsets = (
        (None, {
            'fields': (('title', 'country'),)
        }),
        ('Основная информация', {
            'fields': (('author', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('year', 'date_add'),)
        }),
        (None, {
            'fields': (('view', 'cover'),)
        }),
        ('О работе', {
            'classes': ('collapse',),
            'fields': (('description',),)
        }),
        ('Опции', {
            'fields': (('url', 'draft'),)
        }),
    )
    form = ProductAdminForm
    inlines = [CollectionInline, ReviewsInline]

    def cover(self, picture):
        return mark_safe(f'<img src={picture.view.url} width="120" height="160"')

    def unpublish(self, request, queryset):
        """Снять работы с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обналена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Снять работы с публикации"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обналена'
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    cover.short_description = 'Обложка'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Работы из коллекции"""
    list_display = ('title', 'product', 'photo_of_works')
    list_display_links = ('title', 'product')
    list_filter = ('product',)
    search_fields = ('title', 'product__title')
    readonly_fields = ('photo_of_works',)
    form = ProductAdminForm

    def photo_of_works(self, picture):
        return mark_safe(f'<img src={picture.image.url} width="60" height="80"')

    photo_of_works.short_description = 'Работы из коллекции'


@admin.register(OverallRating)
class OverallRatingAdmin(admin.ModelAdmin):
    """Рейтинг работ"""
    list_display = ('value', 'id')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('star', 'product', 'id')
    list_display_links = ('star', 'product')
    list_filter = ('star',)
    search_fields = ('star__value',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Рецензии"""
    list_display = ('name', 'parent', 'product', 'email')
    list_display_links = ('name', 'parent', 'product')
    list_filter = ('name', 'product')
    search_fields = ('name', 'product__title')
    fieldsets = (
        (None, {
            'fields': (('name', 'email'),)
        }),
        (None, {
            'fields': (('text',),)
        }),
        ('Комментарий родитель', {
            'fields': (('parent', 'product'),)
        }),
    )
    readonly_fields = ('name', 'parent', 'product', 'email', 'text')


admin.site.site_title = "ArtFusion"
admin.site.site_header = "MyArt"
