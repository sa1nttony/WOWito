from django.urls import path

from .views import (AnnouncementList, AnnouncementDetailView, AnnouncementCreate,
                    AnnouncementUpdate, AnnouncementDelete, ResponseCreate)

urlpatterns = [
    path('', AnnouncementList.as_view(), name='announcements_list'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcements_detail'),
    path('create/', AnnouncementCreate.as_view(), name='announcements_create'),
    path('<int:pk>/update/', AnnouncementUpdate.as_view(), name='announcements_update'),
    path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='announcements_delete'),
    path('<int:pk>/add_response/', ResponseCreate.as_view(), name='response_create'),
]