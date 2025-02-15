from django.urls import path, include

urlpatterns = [
    path('user/', include('app_user.urls')),
    path('poll/', include('poll.urls')),
    path('candidate/', include('candidate.urls')),
    path('voting/', include('votes.urls'))
]
