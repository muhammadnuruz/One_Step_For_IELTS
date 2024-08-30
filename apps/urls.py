from django.urls import path, include

urlpatterns = [
    path('words/', include("apps.words.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
    path('audios/', include("apps.audios.urls")),
]
