
from django.urls import path
from apps.productsexpenses.api.views import *


urlpatterns = [
    path('create/', ProductExpensesCreateView.as_view(), name='productexpenses_create'),
    path('list/', ProductExpensesListView.as_view(), name='productexpenses_list'),
    path('detail/<int:id>', ProductExpensesDetailView.as_view(), name='productexpenses_detail'),
    path('update/<int:id>', ProductExpensesUpdateView.as_view(), name='productexpenses_update'),
    path('delete/<int:id>', ProductExpensesDeleteView.as_view(), name='productexpenses_delete'),
]