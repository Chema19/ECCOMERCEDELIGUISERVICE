from django.urls import path
from apps.expenses.api.views import *


urlpatterns = [
    path('create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('list/', ExpenseListView.as_view(), name='expense_list'),
    path('detail/<int:id>', ExpenseDetailView.as_view(), name='expense_detail'),
    path('update/<int:id>', ExpenseUpdateView.as_view(), name='expense_update'),
    path('delete/<int:id>', ExpenseDeleteView.as_view(), name='expense_delete'),
]