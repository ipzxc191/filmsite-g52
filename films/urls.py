from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('stats/', views.catalog_stats, name='catalog_stats'),
    path('films/', views.film_list, name='film_list'),
    path('films/add/', views.add_film, name='add_film'),
    path('films/search/', views.search_film, name='search_film'),
    path('films/<slug:slug>/', views.film_detail, name='film_detail'),
    path('films/<slug:slug>/review/', views.add_review, name='add_review'),
    path('directors/top/', views.top_directors, name='top_directors'),
    path('directors/<slug:slug>/', views.director_detail, name='director_detail'),
]