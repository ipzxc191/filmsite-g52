# films/views.py
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse


FILMS = {
    1: 'Крёстный отец',
    2: 'Список Шиндлера',
    3: 'Побег из Шоушенка',
}


def index(request):
    return HttpResponse('Добро пожаловать на сайт фильмов!')


def about(request):
    return HttpResponse('Сайт-каталог фильмов. Здесь собраны лучшие фильмы всех времён.')


def film_list(request):
    genre = request.GET.get('genre', '')
    year = request.GET.get('year', '')
    response_text = f'Жанр: {genre}, год: {year}' if genre or year else 'Все фильмы'
    return HttpResponse(response_text)


def film_detail(request, film_id):
    if film_id not in FILMS:
        raise Http404(f'Фильм с id={film_id} не найден')
    return HttpResponse(f'Фильм: {FILMS[film_id]}')


def add_film(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            return HttpResponse('Название фильма не может быть пустым.', status=400)
        return redirect(reverse('film_list'))
    return HttpResponse('Здесь будет форма добавления фильма.')


def search_film(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return HttpResponse('Введите название фильма для поиска.', status=400)
    
    return HttpResponse(f'Результаты поиска по запросу: {query}')


def director_detail(request, director_id):
    return HttpResponse(f'Страница режиссёра с id={director_id}')


def page_not_found(request, exception):
    return HttpResponse('Страница не найдена.', status=404)


def server_error(request):
    return HttpResponse('Произошла ошибка сервера.', status=500)