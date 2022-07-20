from rest_framework import serializers
from apps.core.models import *


class CreditCustomerSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=500)
    deuda = serializers.DecimalField(max_digits=15, decimal_places=2)

class SaleDetailByDayReportSerializer(serializers.Serializer):
    producto = serializers.CharField(max_length=100)
    cantidad = serializers.DecimalField(max_digits=15, decimal_places=2)
    precio = serializers.DecimalField(max_digits=15, decimal_places=2)
    precio_total = serializers.DecimalField(max_digits=15, decimal_places=2)

class SaleByDayReportSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=100)
    fecha_venta = serializers.DateField()
    tipo_pago = serializers.CharField(max_length=100)
    tipo_estado_producto = serializers.CharField(max_length=100)
    tipo_moneda = serializers.CharField(max_length=100)
    tienda = serializers.CharField(max_length=100)
    cliente = serializers.CharField(max_length=100)
    trabajador = serializers.CharField(max_length=100)
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    sale_detail = SaleDetailByDayReportSerializer(many=True)


class SaleByDayFunctionSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=100)
    fecha_venta = serializers.DateField()
    tipo_pago = serializers.CharField(max_length=100)
    tipo_estado_producto = serializers.CharField(max_length=100)
    tipo_moneda = serializers.CharField(max_length=100)
    tienda = serializers.CharField(max_length=100)
    cliente = serializers.CharField(max_length=100)
    trabajador = serializers.CharField(max_length=100)
    total = serializers.DecimalField(max_digits=15, decimal_places=2)

class StockProductByStoreReportSerializer(serializers.Serializer):
    producto = serializers.CharField(max_length=200)
    empresa = serializers.CharField(max_length=200)
    tienda = serializers.CharField(max_length=200)
    tiendaid = serializers.IntegerField()
    entrega = serializers.DecimalField(max_digits=15, decimal_places=2)
    movimientoentrada = serializers.DecimalField(max_digits=15, decimal_places=2)
    movimientosalida = serializers.DecimalField(max_digits=15, decimal_places=2)
    compra = serializers.DecimalField(max_digits=15, decimal_places=2)

class SalePurchaseMovementsByStoreReportSerializer(serializers.Serializer):
    tipo = serializers.CharField(max_length=200)
    id = serializers.CharField(max_length=200)
    codigo = serializers.CharField(max_length=200)
    tienda = serializers.CharField(max_length=200)
    tiendaid = serializers.IntegerField()
    fecha = serializers.CharField(max_length=200)
    producto = serializers.CharField(max_length=200)
    productoid = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=15, decimal_places=2)

class ProductByBrandReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=200)
    empresa_id = serializers.IntegerField()
    empresa = serializers.CharField(max_length=200)
    nombre_comercial = serializers.CharField(max_length=200)