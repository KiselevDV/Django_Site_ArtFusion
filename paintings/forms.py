from django import forms

from .models import Reviews  # Импортируем модель отзывов


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Reviews  # От какой моделт строим форму
        fields = ('name', 'text', 'email')  # Какие поля передаём в форму
