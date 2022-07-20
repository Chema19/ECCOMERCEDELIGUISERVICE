from django.urls import path
from apps.typespayments.api.views import *


urlpatterns = [
    path('create/', TypePaymentCreateView.as_view(), name='typepayment_create'),
    path('list/', TypePaymentListView.as_view(), name='typepayment_list'),
    path('update/<int:id>', TypePaymentUpdateView.as_view(), name='typepayment_update'),
    path('delete/<int:id>', TypePaymentDeleteView.as_view(), name='typepayment_delete'),
]