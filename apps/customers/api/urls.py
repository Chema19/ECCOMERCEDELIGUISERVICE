from django.urls import path
from apps.customers.api.views import *


urlpatterns = [
    path('create/', CustomerCreateView.as_view(), name='customer_create'),
    path('list/', CustomerListView.as_view(), name='customer_list'),
    path('detail/<int:id>', CustomerDetailView.as_view(), name='customer_detail'),
    path('update/<int:id>', CustomerUpdateView.as_view(), name='customer_update'),
    path('delete/<int:id>', CustomerDeleteView.as_view(), name='customer_delete'),
]