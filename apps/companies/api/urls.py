from django.urls import path
from apps.companies.api.views import *


urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('list/', CompanyListView.as_view(), name='company_list'),
    path('detail/<int:id>', CompanyDetailView.as_view(), name='company_detail'),
    path('update/<int:id>', CompanyUpdateView.as_view(), name='company_update'),
    path('delete/<int:id>', CompanyDeleteView.as_view(), name='company_delete'),
]