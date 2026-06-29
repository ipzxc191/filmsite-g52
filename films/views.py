# films/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse('Добро пожаловать на сайт фильмов!')


def about(request):
    return HttpResponse('Сайт-каталог фильмов. Здесь собраны лучшие фильмы всех времён.')


def film_list(request):
    return HttpResponse('Список фильмов — скоро здесь будет каталог.')


def film_detail(request, film_id):
    return HttpResponse(f'Страница фильма с id={film_id}')

def director_detail(request, director_id):
    return HttpResponse(f'Страница режиссёра с id={director_id}')