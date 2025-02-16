from django.urls import path
from .views import VoterView

urlpatterns = [
    path("vote", VoterView.create_vote),
    path('votes', VoterView.get_all)
]
