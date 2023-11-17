from django.urls import path

from .views import PlayerCreate, code_form

urlpatterns = [
    path('signup', PlayerCreate.as_view(), name='sign_up'),
    path('activate', code_form, name='code_form'),
]