from django import forms
from .models import Film, Review

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'year', 'description', 'director', 'genres']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Поделитесь впечатлениями...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'author_name': 'Ваше имя',
            'text': 'Рецензия',
            'rating': 'Оценка (1–10)',
        }


class ReviewSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        required=False,
        label='Поиск рецензий',
        widget=forms.TextInput(attrs={'placeholder': 'Введите текст для поиска'})
    )
    min_rating = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=10,
        label='Минимальный рейтинг'
    )