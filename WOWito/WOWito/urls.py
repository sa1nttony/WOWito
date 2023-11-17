"""
URL configuration for WOWito project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site
from django.contrib.auth.views import LogoutView

from board.views import home_view

urlpatterns = [
    path('admin/filebrowser', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('board.urls_accounts')),
    path('tinymce/', include('tinymce.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('players/', include('board.urls_player')),
    path('announcements/', include('board.urls_announcements')),
    path('logout/', LogoutView.as_view(next_page='/home/'), name='logout'),
    path('home/', home_view, name='home_view'),
    path('responses/', include('board.urls_responses')),
    path('news/', include('board.urls_new')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
