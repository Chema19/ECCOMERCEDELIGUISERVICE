from django.urls import path
from apps.deliveries.api.views import *


urlpatterns = [
    path('create/', DeliveryCreateView.as_view(), name='delivery_create'),
    path('list/', DeliveryListView.as_view(), name='delivery_list'),
    path('listbycustomer/', DeliveryByCustomerListView.as_view(), name='deliverybycustomer_list'),
    path('listproductstockcustomer/', ProductStockCustomerListView.as_view(), name='delivery_listproductstockcustomer'),
    path('detail/<int:id>', DeliveryDetailView.as_view(), name='delivery_detail'),
    path('update/<int:id>', DeliveryUpdateView.as_view(), name='delivery_update'),
    path('delete/<int:id>', DeliveryDeleteView.as_view(), name='delivery_delete'),
]