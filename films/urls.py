from django.urls import path
from . import views

app_name = 'films'

urlpatterns = [
    # fbv
    path('films/search/', views.search_film, name='search_film'),
    path('directors/top/', views.top_directors, name='top_directors'),
    path('actors/add/', views.add_actor, name='add_actor'),
    
    # cbv
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('stats/', views.CatalogStatsView.as_view(), name='catalog_stats'),
    path('films/', views.FilmListView.as_view(), name='film_list'),
    path('films/add/', views.FilmCreateView.as_view(), name='add_film'),
    path('films/<slug:slug>/', views.FilmDetailView.as_view(), name='film_detail'),
    path('films/<slug:slug>/edit/', views.FilmUpdateView.as_view(), name='film_edit'),
    path('films/<slug:slug>/delete/', views.FilmDeleteView.as_view(), name='film_delete'),
    path('films/<slug:slug>/review/', views.AddReviewView.as_view(), name='add_review'),
    path('directors/add/', views.DirectorCreateView.as_view(), name='director_create'),
    path('directors/<slug:slug>/', views.DirectorDetailView.as_view(), name='director_detail'),
    path('directors/<slug:slug>/edit/', views.DirectorUpdateView.as_view(), name='director_edit'),
    path('directors/<slug:slug>/delete/', views.DirectorDeleteView.as_view(), name='director_delete'),
    
]