from django.urls import path
from apps.typesusers.api.views import *


urlpatterns = [
    path('create/', TypeUserCreateView.as_view(), name='typeuser_create'),
    path('list/', TypeUserListView.as_view(), name='typeuser_list'),
    path('update/<int:id>', TypeUserUpdateView.as_view(), name='typeuser_update'),
    path('delete/<int:id>', TypeUserDeleteView.as_view(), name='typeuser_delete'),
]