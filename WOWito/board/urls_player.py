from django.urls import path

from .views import PlayerView, PlayerDetailView, ResponsesList

urlpatterns = [
    path('', PlayerView.as_view(), name='player_list'),
    path('<int:pk>', PlayerDetailView.as_view(), name='player_detail'),
    path('my_account/', ResponsesList.as_view(), name='my_account'),
]