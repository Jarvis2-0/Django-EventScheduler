#pyright: basic
from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('register/', views.register, name='register'),
    path('event/new/', views.event_create, name='event-create'),
    path('event/<int:pk>/', views.event_detail, name='event-detail'),
    path('event/<int:pk>/update/', views.event_update, name='event-update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event-delete'),
]