
from django.urls import path
from apps.movements.api.views import *


urlpatterns = [
    path('create/', MovementCreateView.as_view(), name='movement_create'),
    path('list/', MovementListView.as_view(), name='movement_list'),
    path('detail/<int:id>', MovementDetailView.as_view(), name='movement_detail'),
    path('update/<int:id>', MovementUpdateView.as_view(), name='movement_update'),
    path('delete/<int:id>', MovementDeleteView.as_view(), name='movement_delete'),
]