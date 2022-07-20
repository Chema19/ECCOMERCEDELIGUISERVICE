from django.urls import path
from apps.uploads.api.views import *


urlpatterns = [
    path('uploadstockproducto/', StockProductoUploadView.as_view(), name='upload_uploadstockproducto'),
]