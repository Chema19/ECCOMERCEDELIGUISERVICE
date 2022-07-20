
from django.urls import path
from apps.permissions.api.views import *


urlpatterns = [
    path('create/', PermissionCreateView.as_view(), name='permissions_create'),
    path('list/', PermissionListView.as_view(), name='permissions_list'),
    path('listpermissionactivity/<int:idtipousuario>', PermissionActivityListView.as_view(), name='permissions_listpermissionactivity'),
    path('detail/<int:id>', PermissionDetailView.as_view(), name='permissions_detail'),
    path('detailpermissionactivity/<int:idtipousuario>/activity/<int:idactividad>', PermissionActivityDetailView.as_view(), name='permissions_detailpermissionactivity'),
    path('update/<int:id>', PermissionUpdateView.as_view(), name='permissions_update'),
    path('delete/<int:id>', PermissionDeleteView.as_view(), name='permissions_delete'),
]