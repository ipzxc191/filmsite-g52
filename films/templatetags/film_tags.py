from django import template
import datetime

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.date.today().year

@register.inclusion_tag('films/includes/latest_films.html')
def latest_films(count=3):
    """Рендерит виджет с последними добавленными фильмами."""
    # Заглушка — в модуле 3 заменим на запрос к БД
    films = [
        {'id': 1, 'title': 'Крёстный отец', 'year': 1972},
        {'id': 2, 'title': 'Список Шиндлера', 'year': 1993},
        {'id': 3, 'title': 'Побег из Шоушенка', 'year': 1994},
    ]
    return {'films': films[:count]}