
from django.urls import path
from apps.sales.api.views import *


urlpatterns = [
    path('create/', SaleCreateView.as_view(), name='sale_create'),
    path('list/', SaleListView.as_view(), name='sale_list'),
    path('detail/<int:id>', SaleDetailView.as_view(), name='sale_detail'),
    path('update/<int:id>', SaleUpdateView.as_view(), name='sale_update'),
    path('updatefieldfacturador/<int:id>', SaleUpdateVoucherFieldView.as_view(), name='sale_updatefieldfacturador'),
    path('delete/<int:id>', SaleDeleteView.as_view(), name='sale_delete'),
]