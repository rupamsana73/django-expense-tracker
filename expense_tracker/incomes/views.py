from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income
from django.shortcuts import get_object_or_404
@login_required(login_url='/')
def income_view(request):

    if request.method == "POST":
        title = request.POST.get('title')
        amount = request.POST.get('amount')

        if title and amount:
            Income.objects.create(
                user=request.user,
                title=title,
                amount=amount
            )
            return redirect('/incomes/')

    incomes = Income.objects.filter(user=request.user).order_by('-date')

    context = {
        'incomes': incomes
    }

    return render(request, 'incomes/incomes.html', context)


@login_required(login_url='/')
def delete_income(request, id):
    income = get_object_or_404(Income, id=id, user=request.user)
    income.delete()
    return redirect('/incomes/')
