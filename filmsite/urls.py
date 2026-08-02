from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from films.forms import CustomAuthenticationForm
from films.views import RegisterView

admin.site.site_header = 'Управление каталогом фильмов'
admin.site.site_title = 'Админка — Сайт фильмов'
admin.site.index_title = 'Панель администратора'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    
    # Восстановление пароля — переопределяем для указания кастомных шаблонов
    path('accounts/password-reset/',
        PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path('accounts/password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path('accounts/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path('accounts/reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('films.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)