from django.urls import path
from .views import expense_view, delete_expense

urlpatterns = [
    path('', expense_view, name='expenses'),
    path('delete/<int:id>/', delete_expense, name='delete_expense'),
]
