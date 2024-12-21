from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newReview/', views.newReview, name='newReview'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
]
