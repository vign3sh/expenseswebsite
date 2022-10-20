from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
from calendar  import monthrange

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    expenses = expenses.order_by('-date')
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        if not date:
            messages.error(request, 'date is required')
            return render(request, 'expenses/add_expense.html', context)
        
        if category=='select an option':
            messages.error(request, 'category is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))
    category_list.sort()

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def expense_category_summary2(request):
    expenses = Expense.objects.filter(owner=request.user)

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))
    category_list.sort()

    def get_month_expense(filtered_by_category,month,year):
       
        amount = 0
        filtered_by_month = filtered_by_category.filter(date__month=month, date__year=year)

        for item in filtered_by_month:
            amount += item.amount
        return amount

    
    results = {}
    MONTHS=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 
    for y in category_list:
        todays_date = datetime.date.today()
        six_months_ago = todays_date-datetime.timedelta(days=30*5+5)

        
        
        year = six_months_ago.year
        month = six_months_ago.month
        res=[]
        filtered_by_category =expenses.filter(category=y)
        month_list=[]
        while year <= todays_date.year and month <= todays_date.month:
            month_list.append(MONTHS[month-1])
            res.append(
                get_month_expense(filtered_by_category,month,year)
            )
            month +=1
            if month==13:
                year=year+1
                month=1
            
        results[y]=(res)

    return JsonResponse({'expense_category_data': results,'months':month_list}, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')


def expense_dashboard(request):
    todays_date = datetime.date.today()
    week= todays_date.isocalendar().week

    expenses = Expense.objects.filter(owner=request.user)
    expenses_today=expenses.filter(date__year = todays_date.year,
            date__month = todays_date.month, date__day = todays_date.day)
    expenses_week=expenses.filter(date__week__gte = week,date__year = todays_date.year)
    expenses_month=expenses.filter(date__year = todays_date.year,
            date__month = todays_date.month)
    
    expenses_year=expenses.filter(date__year = todays_date.year)

    
    

    amount=[0,0,0,0]
    count=[0,0,0,0]
    for x in expenses_today:
        amount[0] += x.amount
        count[0]+=1
    for x in expenses_week:
        amount[1] += x.amount
        count[1]+=1
    for x in expenses_month:
        amount[2] += x.amount
        count[2]+=1
    for x in expenses_year:
        amount[3] += x.amount
        count[3]+=1

    return JsonResponse({'amount': amount, 'count':count}, safe=False)



def expense_summary(request):
    MONTHS=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] 
    todays_date = datetime.date.today()
    year = todays_date.year
    month = todays_date.month

    expenses = Expense.objects.filter(owner=request.user)
    expenses_month=expenses.filter(date__year = year,
            date__month = month)
    
    expenses_year=expenses.filter(date__year = year)

    
    
    no_of_days=monthrange(year, month)[1]
    
    year_amount={}
    month_amount={}

    for x in range(12):
        year_amount[MONTHS[x]]=0.0 
    for x in range(1,no_of_days+1):
        month_amount[x]=0.0
        

    for i in range(1,no_of_days+1):
        exp_month=expenses_month.filter(date__day=i)
        for y in exp_month:
            month_amount[i]+=y.amount
    
    for i in range(12):
        exp_year=expenses_year.filter(date__month=i+1)
        for y in exp_year:
            year_amount[MONTHS[i]]+=y.amount
        
    
    return JsonResponse({'month': month_amount, 'year':year_amount, 'current_month':MONTHS[month-1], 'current_year':year}, safe=False)