# films/views.py
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse


FILMS = [
    {'id': 1, 'title': 'Крёстный отец', 'year': 1972, 'description': 'Классика мирового кино.'},
    {'id': 2, 'title': 'Список Шиндлера', 'year': 1993, 'description': 'История Оскара Шиндлера.'},
    {'id': 3, 'title': 'Побег из Шоушенка', 'year': 1994, 'description': 'История о надежде и свободе.'},
]


def index(request):
    context = {
        'title': 'Лучшие фильмы всех времён',
    }
    return render(request, 'films/index.html', context)


def about(request):
    context = {
        'title': 'О нашем сайте',
        'film_count': len(FILMS),
    }
    return render(request, 'films/about.html', context)


def film_list(request):
    context = {
        'films': FILMS,
        'total': len(FILMS),
    }
    return render(request, 'films/film_list.html', context)


def film_detail(request, film_id):
    film = next((f for f in FILMS if f['id'] == film_id), None)
    if film is None:
        raise Http404('Фильм не найден')
    return render(request, 'films/film_detail.html', {'film': film})


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