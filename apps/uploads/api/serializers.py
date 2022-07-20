from rest_framework import serializers
from apps.core.models import *


class StockProductoDetalleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre_producto = serializers.CharField(max_length=500)
    cantidad = serializers.DecimalField(max_digits=15, decimal_places=2)
    cantidad_tienda = serializers.DecimalField(max_digits=15, decimal_places=2)

class StockProductoLocalSerializer(serializers.Serializer):
    tiendas = serializers.IntegerField()
    fecha = serializers.DateField()
    colaboradores = serializers.IntegerField()
    stock_productos_detalles = StockProductoDetalleSerializer(many=True)