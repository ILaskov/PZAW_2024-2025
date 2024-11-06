from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path('forms/', views.forms, name='forms'),
    path('<str:poll_name>/', views.index, name="poll"),
    path('vote/<str:poll_name>/', views.vote, name="vote"),
    path('results/<str:poll_name>/', views.results, name="results"),
]
