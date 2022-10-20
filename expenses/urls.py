import django


from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    path('search-expenses', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
     path('expense_category_summary2', views.expense_category_summary2,
         name="expense_category_summary2"),
    path('expenses-stats', views.stats_view,
         name="exp-stats"),
     path('expense_dashboard', views.expense_dashboard,
         name="expense_dashboard"),
     path('expense_summary', views.expense_summary,
         name="expense_summary"),
]
