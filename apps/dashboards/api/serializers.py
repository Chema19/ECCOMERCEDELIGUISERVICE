from rest_framework import serializers
from apps.core.models import *

class SaleCountByLocalAndMonthSerializer(serializers.Serializer):
    mes = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class SaleCountByLocalSerializer(serializers.Serializer):
    tiendas = serializers.IntegerField()
    nombre_tienda = serializers.CharField(max_length=500)
    cantidades = SaleCountByLocalAndMonthSerializer(many=True)

class SaleAmountByLocalAndMonthSerializer(serializers.Serializer):
    mes = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=15, decimal_places=2)

class SaleAmountByLocalSerializer(serializers.Serializer):
    tiendas = serializers.IntegerField()
    nombre_tienda = serializers.CharField(max_length=500)
    cantidades = SaleAmountByLocalAndMonthSerializer(many=True)

class StockProductSerializer(serializers.Serializer):
    nombre_producto = serializers.CharField(max_length=500)
    cantidad = serializers.IntegerField()
    precio = serializers.DecimalField(max_digits=15, decimal_places=2)

class StockProductReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre_producto = serializers.CharField(max_length=500)
    cantidad = serializers.IntegerField()

class MovementWithoutApprovalSerializer(serializers.Serializer):
    sin_confirmar_recibido = serializers.IntegerField()
    sin_confirmar_trasportado = serializers.IntegerField()
    sin_confirmar_preparado = serializers.IntegerField()

class DecimalValueSerializer(serializers.Serializer):
    valortotal = serializers.DecimalField(max_digits=15, decimal_places=2)
    valorcredito = serializers.DecimalField(max_digits=15, decimal_places=2)
    valorcontado = serializers.DecimalField(max_digits=15, decimal_places=2)
    valortransferencia = serializers.DecimalField(max_digits=15, decimal_places=2)
    valoramortizacion = serializers.DecimalField(max_digits=15, decimal_places=2)
    valorcreditoamortizacioncontado = serializers.DecimalField(max_digits=15, decimal_places=2)
    valorcreditoamortizaciontransaccion = serializers.DecimalField(max_digits=15, decimal_places=2)

class IntegerValueSerializer(serializers.Serializer):
    valortotal = serializers.IntegerField()
    valorcredito = serializers.IntegerField()
    valorcontado = serializers.IntegerField()
    valoramortizacion = serializers.IntegerField()
    valortransferencia = serializers.IntegerField()
    valoranulados = serializers.IntegerField()



