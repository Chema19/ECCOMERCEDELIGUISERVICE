"""SOLUCIONESAGROMINBACKEND URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

schema_view = get_swagger_view(title='SOLUCIONES AGROMIN API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path('rest-auth/', include('rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('core/', include('apps.core.api.urls')),
    path('users/', include('apps.users.api.urls')),
    path('products/', include('apps.products.api.urls')),
    path('customers/', include('apps.customers.api.urls')),
    path('locals/', include('apps.locals.api.urls')),
    path('sales/', include('apps.sales.api.urls')),
    path('purchases/', include('apps.purchases.api.urls')),
    path('companies/', include('apps.companies.api.urls')),
    path('movements/', include('apps.movements.api.urls')),
    path('typesusers/', include('apps.typesusers.api.urls')),
    path('logins/', include('apps.logins.api.urls')),
    path('dashboards/', include('apps.dashboards.api.urls')),
    path('typespayments/', include('apps.typespayments.api.urls')),
    path('typesstatesproducts/', include('apps.typesstatesproducts.api.urls')),
    path('typescoins/', include('apps.typescoins.api.urls')),
    path('deliveries/', include('apps.deliveries.api.urls')),
    path('expenses/', include('apps.expenses.api.urls')),
    path('productsexpenses/', include('apps.productsexpenses.api.urls')),
    path('activities/', include('apps.activities.api.urls')),
    path('permissions/', include('apps.permissions.api.urls')),
    path('uploads/', include('apps.uploads.api.urls')),
    path('reports/', include('apps.reports.api.urls')),
    path('typesproducts/', include('apps.typesproducts.api.urls')),
    path('credits/', include('apps.credits.api.urls')),
    path('portalscustomers/', include('apps.portalscustomers.api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + staticfiles_urlpatterns()
