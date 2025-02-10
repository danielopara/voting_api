from django.urls import path
from .views import PollView

urlpatterns = [
    path('create_poll', PollView.create_poll),
    path('', PollView.get_all_polls)
]
