from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    # cbv
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('stats/', views.CatalogStatsView.as_view(), name='catalog_stats'),
    path('films/add/', views.AddFilmView.as_view(), name='add_film'),
    # fbv
    path('films/', views.film_list, name='film_list'),
    path('films/search/', views.search_film, name='search_film'),
    path('films/<slug:slug>/', views.film_detail, name='film_detail'),
    path('films/<slug:slug>/review/', views.add_review, name='add_review'),
    path('directors/top/', views.top_directors, name='top_directors'),
    path('directors/<slug:slug>/', views.director_detail, name='director_detail'),
    path('actors/add/', views.add_actor, name='add_actor'),
]