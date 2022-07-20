from rest_framework import serializers
from apps.core.models import *

class DeliveryDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=6, decimal_places=2)
    productos = serializers.IntegerField()
    entregas = serializers.IntegerField()
    estado = serializers.CharField(max_length=10)

class DeliverySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    colaboradores_emisor = serializers.IntegerField()
    fue_preparado = serializers.BooleanField()
    colaboradores_transporte = serializers.IntegerField()
    fue_enviado = serializers.BooleanField()
    personas = serializers.IntegerField()
    fue_entregado = serializers.BooleanField()
    tiendas = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1000)
    fecha_entrega = serializers.DateField()
    detalles_entregas = DeliveryDetailSerializer(many=True)
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.IntegerField()

class DeliveryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    fue_preparado = serializers.BooleanField()
    fue_enviado = serializers.BooleanField()
    fue_entregado = serializers.BooleanField()
    personas_id = serializers.IntegerField()
    personas = serializers.CharField(max_length=500)
    tiendas_id = serializers.IntegerField()
    tiendas = serializers.CharField(max_length=500)
    descripcion = serializers.CharField(max_length=1000)
    fecha_entrega = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    proveniencia = serializers.CharField(max_length=500)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()

class StockCustomerDetailSerializer(serializers.Serializer):
    productos = serializers.IntegerField()
    productos_nombre = serializers.CharField(max_length=500)
    cantidad = serializers.IntegerField()

class StockCustomerSerializer(serializers.Serializer):
    personas = serializers.IntegerField()
    personas_nombre = serializers.CharField(max_length=500)
    personas_documento = serializers.CharField(max_length=500)
    personas_celular = serializers.CharField(max_length=500)
    detalles = StockCustomerDetailSerializer(many=True)


