from django.urls import path
from .views import create_candidate, get_candidate

urlpatterns = [
    path('register_candidate', create_candidate),
    path('', get_candidate)   
]
