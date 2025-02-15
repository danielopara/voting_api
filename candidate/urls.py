from django.urls import path
from .views import create_candidate

urlpatterns = [
    path('register_candidate', create_candidate)
]
