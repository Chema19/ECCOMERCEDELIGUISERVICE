from rest_framework import serializers
from apps.core.models import *

class MovementDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cantidad = serializers.DecimalField(max_digits=6, decimal_places=2)
    productos = serializers.IntegerField()
    movimientos = serializers.IntegerField()
    estado = serializers.CharField(max_length=10)

class MovementListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    fue_preparado = serializers.BooleanField()
    fue_enviado = serializers.BooleanField()
    fue_recibido = serializers.BooleanField()
    tiendas_origen_id = serializers.IntegerField()
    tiendas_origen = serializers.CharField(max_length=500)
    tiendas_destino_id = serializers.IntegerField()
    tiendas_destino = serializers.CharField(max_length=500)
    descripcion = serializers.CharField(max_length=1000)
    fecha_movimiento = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()

class MovementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    colaboradores_emisor = serializers.IntegerField()
    fue_preparado = serializers.BooleanField()
    colaboradores_transporte = serializers.IntegerField()
    fue_enviado = serializers.BooleanField()
    colaboradores_receptor = serializers.IntegerField()
    fue_recibido = serializers.BooleanField()
    tiendas_origen = serializers.IntegerField()
    tiendas_destino = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1000)
    fecha_movimiento = serializers.DateField()
    detalles_movimientos = MovementDetailSerializer(many=True)
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()






