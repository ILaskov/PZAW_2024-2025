from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path('new/', views.new_poll, name='new'),
    path('<int:pk>/', views.DetailView.as_view(), name="details"),
    path('<str:poll_id>/', views.single, name="poll"),
    path('vote/<str:poll_id>/', views.vote, name="vote"),
    path('results/<str:poll_id>/', views.results, name="results"),
]
