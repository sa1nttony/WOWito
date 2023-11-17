from django.urls import path

from .views import ResponseDelete

urlpatterns = [
    path('<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
]