from django.contrib import admin
from django.utils.html import format_html
from .models import Film, Genre, Director, Actor, FilmStats


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'rating_badge', 'director', 'genre_list')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'director__name')
    list_filter = ('year', 'genres')
    list_per_page = 20
    empty_value_display = '— не указано —'
    actions = ['reset_rating', 'add_classic_genre']

    @admin.display(description='Рейтинг')
    def rating_badge(self, obj):
        if obj.rating >= 8:
            color = 'green'
        elif obj.rating >= 5:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.rating
        )

    @admin.display(description='Жанры')
    def genre_list(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    @admin.action(description='Сбросить рейтинг выбранных фильмов')
    def reset_rating(self, request, queryset):
        updated_count = queryset.update(rating=0.0)
        self.message_user(request, f'Рейтинг сброшен у {updated_count} фильмов.')

    @admin.action(description='Добавить жанр «Классика»')
    def add_classic_genre(self, request, queryset):
        classic_genre, _ = Genre.objects.get_or_create(
            name='Классика', defaults={'slug': 'klassika'}
        )
        for film in queryset:
            film.genres.add(classic_genre)
        self.message_user(request, f'Жанр «Классика» добавлен к {queryset.count()} фильмам.')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_per_page = 15
    
    
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'film_count')
    search_fields = ('name',)
    empty_value_display = '— нет данных —'
    
    list_per_page = 15
    
    actions = ['clear_bio']

    @admin.display(description='Количество фильмов')
    def film_count(self, obj):
        return obj.films.count()

    @admin.action(description='Очистить биографию выбранных режиссёров')
    def clear_bio(self, request, queryset):
        updated_count = queryset.update(bio='')
        self.message_user(request, f'Биография очищена у {updated_count} режиссёров.')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FilmStats)
class FilmStatsAdmin(admin.ModelAdmin):
    list_display = ('film', 'views_count', 'likes_count')