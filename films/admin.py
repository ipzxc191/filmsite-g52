from django.contrib import admin
from .models import Film, Genre, Director, Actor, FilmStats


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'rating', 'director')
    list_display_links = ('title',)
    list_editable = ('rating',)
    list_per_page = 20
    empty_value_display = '— не указано —'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_editable = ('slug',)
    list_per_page = 15


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = '— нет данных —'
    list_per_page = 15


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(FilmStats)
class FilmStatsAdmin(admin.ModelAdmin):
    list_display = ('film', 'views_count', 'likes_count')