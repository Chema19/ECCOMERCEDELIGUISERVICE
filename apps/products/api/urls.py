
from django.urls import path
from apps.products.api.views import *


urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('list/', ProductListView.as_view(), name='product_list'),
    path('detail/<int:id>', ProductDetailView.as_view(), name='product_detail'),
    path('update/<int:id>', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:id>', ProductDeleteView.as_view(), name='product_delete'),
]