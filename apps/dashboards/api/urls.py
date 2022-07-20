from django.urls import path
from apps.dashboards.api.views import *


urlpatterns = [
    path('salescountbylocalandmonth/', SaleCountByLocalAndMonthListView.as_view(), name='SaleCountByLocalAndMonth_list'),
    path('salesamonthbylocalandmonth/', SaleAmonthByLocalAndMonthListView.as_view(), name='SaleAmonthByLocalAndMonth_list'),
    path('stockbyproducto/<int:id>', StockProductByLocalListView.as_view(),
         name='StockByProduct_list'),
    path('stockbyproductoreport/<int:id>/fecha/<str:fecha>', StockProductByLocalReportListView.as_view(),
         name='StockByProductReport_list'),
    path('movementwithoutapprovaltransportandpreparation/', MovementWithoutApprovalTransportationAndPreparationDetailView.as_view(),
         name='MovementWithoutApprovalTransportationAndPreparation_detail'),
    path('saleamounthsolesbylocalanddaily/<int:id>', SaleAmountSolesByLocalAndDailyDataView.as_view(), name='SaleAmountSolesByLocalAndDaily_data'),
    path('saleacountsolesbylocalanddaily/<int:id>', SaleCountSolesByLocalAndDailyDataView.as_view(), name='SaleCountSolesByLocalAndDailyDataView_data'),
    path('saleamounthdolaresbylocalanddaily/<int:id>', SaleAmountDolaresByLocalAndDailyDataView.as_view(),name='SaleAmountDolaresByLocalAndDaily_data'),
    path('saleacountdolaresbylocalanddaily/<int:id>', SaleCountDolaresByLocalAndDailyDataView.as_view(),name='SaleCountDolaresByLocalAndDailyDataView_data'),
    path('salediscountbylocalanddaily/<int:id>', SaleDiscountByLocalAndDailyDataView.as_view(),
         name='SaleDiscountByLocalAndDailyDataView_data'),
]