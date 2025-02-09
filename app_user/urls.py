from django.urls import path

from .views import UserView

urlpatterns = [
    # register user
    path('register', UserView.register),
    
    # get list of users
    path('users', UserView.get_users),
    path('<str:usr_id>', UserView.get_user_by_id)
]
