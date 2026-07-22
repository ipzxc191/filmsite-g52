# films/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Film, Genre, Director, Actor, FilmStats


class FilmStatsInline(admin.TabularInline):
    model = FilmStats
    extra = 0


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('poster_thumbnail', 'title', 'year', 'rating_badge', 'director', 'genre_list')
    list_display_links = ('title',)
    search_fields = ('title', 'description', 'director__name')
    list_filter = ('year', 'genres')
    list_per_page = 20
    empty_value_display = '— не указано —'
    actions = ['reset_rating', 'add_classic_genre']

    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('director', 'genres', 'actors')
    readonly_fields = ('created_at',)
    inlines = [FilmStatsInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'year', 'description', 'poster')
        }),
        ('Участники', {
            'fields': ('director', 'genres', 'actors')
        }),
        ('Рейтинг', {
            'fields': ('rating',),
            'classes': ('collapse',),
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

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
    
    @admin.display(description='Постер')
    def poster_thumbnail(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" width="50" height="70" '
                'style="object-fit: cover; border-radius: 4px;" />',
                obj.poster.url
            )
        return '—'

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
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'film_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('films_preview',)
    actions = ['clear_bio']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug')
        }),
        ('Дополнительно', {
            'fields': ('bio', 'photo', 'films_preview'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Количество фильмов')
    def film_count(self, obj):
        return obj.films.count()

    @admin.display(description='Фильмы режиссёра')
    def films_preview(self, obj):
        return ', '.join(film.title for film in obj.films.all()) or 'Фильмов пока нет'

    @admin.action(description='Очистить биографию выбранных режиссёров')
    def clear_bio(self, request, queryset):
        updated_count = queryset.update(bio='')
        self.message_user(request, f'Биография очищена у {updated_count} режиссёров.')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo')
    search_fields = ('name',)


@admin.register(FilmStats)
class FilmStatsAdmin(admin.ModelAdmin):
    list_display = ('film', 'views_count', 'likes_count')