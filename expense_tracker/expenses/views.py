from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense

@login_required(login_url='/')
def expense_view(request):

    if request.method == "POST":
        title = request.POST.get('title')
        amount = request.POST.get('amount')

        if title and amount:
            Expense.objects.create(
                user=request.user,
                title=title,
                amount=amount
            )
            return redirect('/expenses/')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    context = {
        'expenses': expenses
    }

    return render(request, 'expenses/expenses.html', context)


@login_required(login_url='/')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('/expenses/')


