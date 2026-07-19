from django.contrib import admin
from django.urls import include, path
from django.conf import settings

admin.site.site_header = 'Управление каталогом фильмов'
admin.site.site_title = 'Админка — Сайт фильмов'
admin.site.index_title = 'Панель администратора'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('films.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]