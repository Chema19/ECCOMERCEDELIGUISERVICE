from rest_framework import serializers
from apps.core.models import *

class PurchaseDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2)
    productos = serializers.IntegerField()
    compras = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    cambiar_precio = serializers.BooleanField()
    precio_unitario_compra = serializers.DecimalField(max_digits=10, decimal_places=2)
    tipo_cambio = serializers.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_ganancia = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario_soles = serializers.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = serializers.DecimalField(max_digits=10, decimal_places=2)
    estado = serializers.CharField(max_length=10)

class PurchaseListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    personas = serializers.CharField(max_length=500)
    personas_id = serializers.IntegerField()
    tiendas = serializers.CharField(max_length=500)
    tiendas_id = serializers.IntegerField()
    fecha_compra = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()

class PurchaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    personas = serializers.IntegerField()
    colaboradores = serializers.IntegerField()
    tiendas = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1000)
    fecha_compra = serializers.DateField()
    detalles_compras = PurchaseDetailSerializer(many=True)
    tipomonedas = serializers.IntegerField()
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()





