from .models import Film, Genre


class FilmQuerySetMixin:
    def get_queryset(self):
        return Film.objects.select_related('director').prefetch_related('genres', 'actors')


class RecentFilmsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_films'] = Film.objects.recent(3)
        return context
    
    
class FilmEditMixin:
    """Общие настройки для создания и редактирования фильмов."""
    from .models import Film
    from .forms import FilmForm
    model = Film
    form_class = FilmForm
    template_name = 'films/film_form.html'


class GenreListMixin:
    """Добавляет список всех жанров в контекст."""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context