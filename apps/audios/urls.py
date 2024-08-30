from django.urls import path

from apps.audios.views import AudiosDetailViewSet, AudiosListViewSet

urlpatterns = [
    path('detail/<int:pk>/', AudiosDetailViewSet.as_view(), name='audios-detail'),
    path('<int:section>/<str:type>/', AudiosListViewSet.as_view(), name="audios-list")
]
