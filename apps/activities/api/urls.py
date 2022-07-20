
from django.urls import path
from apps.activities.api.views import *


urlpatterns = [
    path('create/', ActivityCreateView.as_view(), name='activity_create'),
    path('list/', ActivityListView.as_view(), name='activity_list'),
    path('detail/<int:id>', ActivityDetailView.as_view(), name='activity_detail'),
    path('update/<int:id>', ActivityUpdateView.as_view(), name='activity_update'),
    path('delete/<int:id>', ActivityDeleteView.as_view(), name='activity_delete'),
]