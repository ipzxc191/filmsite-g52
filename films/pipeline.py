from .models import UserProfile


def create_user_profile(backend, user, response, *args, **kwargs):
    """Создаёт UserProfile при первом входе через OAuth, если его нет."""
    UserProfile.objects.get_or_create(user=user)