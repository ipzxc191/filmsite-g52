from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('films/', views.film_list, name='film_list'),
    path('films/<int:film_id>/', views.film_detail, name='film_detail'),
    path('directors/<int:director_id>/', views.director_detail, name='director_detail'),
]