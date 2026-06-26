from django.urls import path
from .views import login, user_list

urlpatterns = [
    path('login/', login, name='login'),
    path('users/', user_list, name='user-list'),
]
