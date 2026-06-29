from django.http import HttpResponse


def index(request):
    return HttpResponse('Добро пожаловать на сайт фильмов!')


def about(request):
    return HttpResponse('Сайт-каталог фильмов. Здесь собраны лучшие фильмы всех времён.')