
from django.urls import path
from apps.purchases.api.views import *


urlpatterns = [
    path('create/', PurchaseCreateView.as_view(), name='compra_create'),
    path('list/', PurchaseListView.as_view(), name='compra_list'),
    path('detail/<int:id>', PurchaseDetailView.as_view(), name='compra_detail'),
    path('update/<int:id>', PurchaseUpdateView.as_view(), name='compra_update'),
    path('delete/<int:id>', PurchaseDeleteView.as_view(), name='compra_delete'),
]