from django import forms
from .models import Actor, Film, Review

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'year', 'description', 'director', 'genres', 'poster']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if title.strip().isdigit():
            raise forms.ValidationError('Название фильма не может состоять только из цифр.')
        return title

    def clean(self):
        cleaned_data = super().clean()
        genres = cleaned_data.get('genres')

        if genres:
            genre_names = [genre.name for genre in genres]
            if 'Комедия' in genre_names and 'Трагедия' in genre_names:
                self.add_error('genres', 'Жанры «Комедия» и «Трагедия» не могут быть выбраны одновременно.')

        return cleaned_data


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
        
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text.split()) < 5:
            raise forms.ValidationError(
                'Рецензия слишком короткая — напишите хотя бы 5 слов.'
            )
        return text
    
    def clean_author_name(self):
        name = self.cleaned_data['author_name']
        if name.strip().lower() == 'анонимный критик':
            raise forms.ValidationError('Это имя зарезервировано системой, выберите другое.')
        return name.strip()
    
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text')

        if rating and rating <= 3 and text and len(text) < 50:
            raise forms.ValidationError(
                'Для низкой оценки (3 и ниже) распишите причину подробнее — минимум 50 символов.'
            )

        return cleaned_data


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
    
class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'photo']