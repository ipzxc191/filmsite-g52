# films/models.py
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from slugify import slugify

from films.validators import validate_film_year



class Director(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    bio = models.TextField(blank=True, verbose_name='Биография')
    photo = models.ImageField(upload_to='directors/', blank=True, verbose_name='Фото')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Director.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('films:director_detail', kwargs={'slug': self.slug})
    
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
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(director__name__icontains=query)
        ).distinct()


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    year = models.PositiveIntegerField(validators=[validate_film_year], verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='Рейтинг')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    director = models.ForeignKey(
        'Director', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='films', verbose_name='Режиссёр'
    )
    genres = models.ManyToManyField('Genre', blank=True, related_name='films', verbose_name='Жанры')
    actors = models.ManyToManyField('Actor', blank=True, related_name='films', verbose_name='Актёры')

    objects = FilmManager()

    class Meta:
        ordering = ['-year']
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title} ({self.year})'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Film.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('films:film_detail', kwargs={'slug': self.slug})

    
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
    
    
class Review(models.Model):
    film = models.ForeignKey(
        Film, on_delete=models.CASCADE, related_name='reviews', verbose_name='Фильм'
    )
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    text = models.TextField(verbose_name='Текст рецензии')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Оценка от 1 до 10'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'

    def __str__(self):
        return f'Рецензия на «{self.film.title}» от {self.author_name}'