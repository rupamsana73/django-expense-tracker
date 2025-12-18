from django.urls import path
from .views import auth_view, logout_view

urlpatterns = [
    path('', auth_view, name='auth'),
    path('logout/', logout_view, name='logout'),
]



