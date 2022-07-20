from django.urls import path
from apps.reports.api.views import *


urlpatterns = [
    path('creditcustomerlistreport/', CreditCustomerListView.as_view(), name='list_creditcustomerlistreport'),
    path('salebydayreport/', SalesByDayReportView.as_view(), name='list_salebydayreport'),
    path('salepurchasemovementbystorereport/', SalePurchaseMovementsByStoreReportView.as_view(), name='list_salepurchasemovementbystorereport'),
    path('stockproductbystorereport/', StockProductByStoreReportView.as_view(), name='list_stockproductbystorereport'),
    path('productbybrandreport/', ProductsByBrandReportView.as_view(), name='list_productbybrandreport'),
]