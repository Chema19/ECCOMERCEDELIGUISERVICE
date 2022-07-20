from django.urls import path
from apps.typesstatesproducts.api.views import *


urlpatterns = [
    path('create/', TypeStateProductCreateView.as_view(), name='typestateproduct_create'),
    path('list/', TypeStateProductListView.as_view(), name='typestateproduct_list'),
    path('update/<int:id>', TypeStateProductUpdateView.as_view(), name='typestateproduct_update'),
    path('delete/<int:id>', TypeStateProductDeleteView.as_view(), name='typestateproduct_delete'),
]