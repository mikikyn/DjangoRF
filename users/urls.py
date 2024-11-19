from django.urls import path
from . import views
from .views import confirm_user_view

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorization/', views.authorization_api_view),
    path('api/v1/users/confirm/', confirm_user_view, name='confirm_user'),
]
