from django.urls import path
from apps.logins.api.views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]