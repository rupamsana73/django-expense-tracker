from django.urls import path
from .views import income_view, delete_income

urlpatterns = [
    path('', income_view, name='incomes'),
    path('delete/<int:id>/', delete_income, name='delete_income'),
]



