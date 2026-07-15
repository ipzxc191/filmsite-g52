# films/views.py
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import F, Avg, Count, Max, Min

from films.models import Director, Film, FilmStats


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
    film = get_object_or_404(
        Film.objects.select_related('director').prefetch_related('genres', 'actors'),
        id=film_id
    )
    
    FilmStats.objects.filter(film=film).update(views_count=F('views_count') + 1)
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
    director = get_object_or_404(Director, id=director_id)
    films = director.films.select_related('director').prefetch_related('genres')
    context = {
        'director': director,
        'films': films,
    }
    return render(request, 'films/director_detail.html', context)


def top_directors(request):
    directors = Director.objects.annotate(
        avg_rating=Avg('films__rating'),
        film_count=Count('films', distinct=True)
    ).filter(
        film_count__gte=2
    ).order_by(
        '-avg_rating'
    )[:5]

    context = {'directors': directors}
    return render(request, 'films/top_directors.html', context)


def catalog_stats(request):
    overall_stats = Film.objects.aggregate(
        total=Count('id'),
        avg_rating=Avg('rating'),
        max_rating=Max('rating'),
        min_rating=Min('rating'),
    )

    top_directors = Director.objects.annotate(
        film_count=Count('films')
    ).filter(film_count__gt=0).order_by('-film_count')[:5]

    films_by_year = Film.objects.values('year').annotate(
        count=Count('id')
    ).order_by('-year')

    context = {
        'overall_stats': overall_stats,
        'top_directors': top_directors,
        'films_by_year': films_by_year,
    }
    return render(request, 'films/catalog_stats.html', context)


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