from django.urls import path
from .views import dashboard_view, export_transactions

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('export/', export_transactions, name='export_transactions'),
]

