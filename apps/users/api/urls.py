""" URLs related to user app"""

from django.urls import path
from apps.users.api.views import *


urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('detail/<int:id>', UserDetailView.as_view(), name='user_detail'),
    path('personas/', PersonSelectListView.as_view(), name='persona_list'),
    path('detailpersona/<int:id>', PersonGetDetailView.as_view(), name='detailpersona'),
    path('update/<int:id>', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:id>', UserDeleteView.as_view(), name='user_delete'),
]