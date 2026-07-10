# films/models.py
from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(
        upload_to='directors/',
        blank=True,
        verbose_name='Фото'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    photo = models.ImageField(
        upload_to='actors/',
        blank=True,
        verbose_name='Фото'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class FilmManager(models.Manager):

    def high_rated(self):
        return self.filter(rating__gte=8.0)

    def by_year(self, year):
        return self.filter(year=year)

    def recent(self, count=5):
        return self.order_by('-created_at')[:count]

    def search(self, query):
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        verbose_name='Рейтинг'
    )
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    # Many-to-One: у фильма один режиссёр
    director = models.ForeignKey(
        Director,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='films',
        verbose_name='Режиссёр'
    )

    # Many-to-Many: у фильма много жанров
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='films',
        verbose_name='Жанры'
    )

    # Many-to-Many: у фильма много актёров
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        related_name='films',
        verbose_name='Актёры'
    )

    objects = FilmManager()

    class Meta:
        ordering = ['-year']
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title} ({self.year})'
    
class FilmStats(models.Model):
    film = models.OneToOneField(
        Film,
        on_delete=models.CASCADE,
        related_name='stats',
        verbose_name='Фильм'
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')

    class Meta:
        verbose_name = 'Статистика фильма'
        verbose_name_plural = 'Статистика фильмов'

    def __str__(self):
        return f'Статистика: {self.film.title}'