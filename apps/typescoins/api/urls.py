from django.urls import path
from apps.typescoins.api.views import *


urlpatterns = [
    path('create/', TypeCoinCreateView.as_view(), name='typecoin_create'),
    path('list/', TypeCoinListView.as_view(), name='typecoin_list'),
    path('detail/<int:id>', TypeCoinDetailView.as_view(), name='typecoin_detail'),
    path('update/<int:id>', TypeCoinUpdateView.as_view(), name='typecoin_update'),
    path('delete/<int:id>', TypeCoinDeleteView.as_view(), name='typecoin_delete'),
]