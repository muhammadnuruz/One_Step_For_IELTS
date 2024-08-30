from django.urls import path

from apps.words.views import WordsDetailViewSet, WordsListViewSet

urlpatterns = [
    path('detail/<int:pk>/', WordsDetailViewSet.as_view(), name='words-detail'),
    path('<str:level>', WordsListViewSet.as_view(), name="words-list")
]
