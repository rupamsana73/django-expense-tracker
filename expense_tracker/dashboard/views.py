from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from incomes.models import Income
from expenses.models import Expense
from django.db.models import Sum
from django.http import HttpResponse
import json
import csv


@login_required(login_url='/')
def dashboard_view(request):

    incomes = Income.objects.filter(user=request.user).order_by('date')
    expenses = Expense.objects.filter(user=request.user).order_by('date')

    # ---------- TOTALS ----------
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # ---------- SIMPLE CHART DATA (STABLE) ----------
    income_amounts = list(incomes.values_list('amount', flat=True))
    expense_amounts = list(expenses.values_list('amount', flat=True))

    labels = list(range(1, max(len(income_amounts), len(expense_amounts)) + 1))

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,

        'recent_incomes': incomes[::-1][:5],
        'recent_expenses': expenses[::-1][:5],

        'chart_labels': json.dumps(labels),
        'income_amounts': json.dumps(income_amounts),
        'expense_amounts': json.dumps(expense_amounts),
    }

    return render(request, 'dashboard/dashboard.html', context)


# =====================================================
# EXPORT ALL TRANSACTIONS → EXCEL (CSV)
# =====================================================

@login_required(login_url='/')
def export_transactions(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_transactions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type', 'Title', 'Amount', 'Date'])

    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    for inc in incomes:
        writer.writerow(['Credit', inc.title, inc.amount, inc.date])

    for exp in expenses:
        writer.writerow(['Debit', exp.title, exp.amount, exp.date])

    return response






