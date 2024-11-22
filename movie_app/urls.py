from django.urls import path
from .views import (
    DirectorListCreateView, DirectorDetailView,
    MovieListCreateView, MovieDetailView,
    ReviewListCreateView, ReviewDetailView,
    TestAPIView
)

urlpatterns = [
    path('directors/', DirectorListCreateView.as_view(), name='director-list-create'),
    path('directors/<int:pk>/', DirectorDetailView.as_view(), name='director-detail'),
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('test/', TestAPIView.as_view(), name='test-api'),
]
