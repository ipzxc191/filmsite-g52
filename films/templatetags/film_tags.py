from django import template
import datetime

from films.models import Film

register = template.Library()


@register.simple_tag
def current_year():
    return datetime.date.today().year

@register.inclusion_tag('films/includes/latest_films.html')
def latest_films(count=3):
    films = Film.objects.recent(count)
    return {'films': films}