
from django.urls import path
from apps.credits.api.views import *


urlpatterns = [
    path('listdebts/', DebtPersonListView.as_view(), name='sale_listdebts'),
    path('createcreditsale/', CreditSaleCreateView.as_view(), name='creditsale_create'),
    path('listcreditbycustomersale/', CreditSaleByCustomerListView.as_view(), name='creditsalebycustomer_list'),
    path('listcreditsale/', CreditSaleListView.as_view(), name='creditsale_list'),
    path('detailcreditsale/<int:id>', CreditSaleDetailView.as_view(), name='creditsale_detail'),
    path('updatecreditsale/<int:id>', CreditSaleUpdateView.as_view(), name='creditsale_update'),
    path('deletecreditsale/<int:id>', CreditSaleDeleteView.as_view(), name='creditsale_delete'),
]