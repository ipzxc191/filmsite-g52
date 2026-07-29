from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    Аутентификация по email вместо username.
    Наследуем ModelBackend, чтобы переиспользовать логику проверки пароля
    и разрешений — переопределяем только метод поиска пользователя.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # username здесь — это то, что ввёл пользователь в поле «Имя пользователя»
        # мы трактуем это значение как email
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Если несколько пользователей с одинаковым email — берём первого
            # В реальном проекте стоит логировать такую ситуацию
            user = User.objects.filter(email=username).first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None