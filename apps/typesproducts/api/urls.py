from django.urls import path
from apps.typesproducts.api.views import *


urlpatterns = [
    path('create/', TypeProductCreateView.as_view(), name='typeproduct_create'),
    path('list/', TypeProductListView.as_view(), name='typeproduct_list'),
    path('update/<int:id>', TypeProductUpdateView.as_view(), name='typeproduct_update'),
    path('delete/<int:id>', TypeProductDeleteView.as_view(), name='typeproduct_delete'),
]