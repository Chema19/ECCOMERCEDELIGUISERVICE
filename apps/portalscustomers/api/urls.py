from django.urls import path
from apps.portalscustomers.api.views import *


urlpatterns = [
    path('create/', PortalCustomerCreateView.as_view(), name='portalcustomer_create'),
    path('list/', PortalCustomerListView.as_view(), name='portalcustomer_list'),
    path('update/<int:id>', PortalCustomerUpdateView.as_view(), name='portalcustomer_update'),
    path('delete/<int:id>', PortalCustomerDeleteView.as_view(), name='portalcustomer_delete'),
]