# films/context_processors.py
from .models import Film, Genre


def catalog_stats(request):
    """
    Добавляет базовую статистику каталога в контекст каждого шаблона.
    Вызывается при каждом запросе — запросы должны быть лёгкими.
    """
    return {
        'total_films': Film.objects.count(),
        'total_genres': Genre.objects.count(),
    }
    
def user_profile(request):
    """
    Добавляет профиль авторизованного пользователя в контекст.
    Для анонимных пользователей — None.
    """
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Exception:
            profile = None
        return {'user_profile': profile}
    return {'user_profile': None}