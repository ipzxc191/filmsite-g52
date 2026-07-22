from datetime import date
from django.core.exceptions import ValidationError


def validate_film_year(value):
    current_year = date.today().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше текущего ({current_year}).'
        )
    if value < 1888:
        raise ValidationError(
            'Год выпуска не может быть раньше 1888 года — до этого кинематографа не существовало.'
        )