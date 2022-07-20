from django.urls import path
from apps.locals.api.views import *


urlpatterns = [
    path('create/', LocalCreateView.as_view(), name='local_create'),
    path('list/', LocalListView.as_view(), name='local_list'),
    path('detail/<int:id>', LocalDetailView.as_view(), name='local_detail'),
    path('update/<int:id>', LocalUpdateView.as_view(), name='local_update'),
    path('delete/<int:id>', LocalDeleteView.as_view(), name='local_delete'),
]