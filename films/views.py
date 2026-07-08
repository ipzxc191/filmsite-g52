# films/views.py
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from films.models import Film


def index(request):
    context = {
        'title': 'Лучшие фильмы всех времён',
    }
    return render(request, 'films/index.html', context)


def film_list(request):
    films = Film.objects.all()
    context = {
        'films': films,
    }
    return render(request, 'films/film_list.html', context)


def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)
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

    films = Film.objects.search(query)
    context = {
        'films': films,
        'query': query,
    }
    return render(request, 'films/search_results.html', context)


def director_detail(request, director_id):
    return HttpResponse(f'Страница режиссёра с id={director_id}')


def about(request):
    context = {
        'title': 'О нашем сайте',
        'film_count': Film.objects.count(),
    }
    return render(request, 'films/about.html', context)


def page_not_found(request, exception):
    return HttpResponse('Страница не найдена.', status=404)


def server_error(request):
    return HttpResponse('Произошла ошибка сервера.', status=500)