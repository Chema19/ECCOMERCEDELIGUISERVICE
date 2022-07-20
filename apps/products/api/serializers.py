from rest_framework import serializers
from apps.core.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProductListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=500)
    precio_base = serializers.DecimalField(max_digits=30, decimal_places=2)
    tipoproductos_id = serializers.IntegerField()
    tipoproductos = serializers.CharField(max_length=500)
    empresas_id = serializers.IntegerField()
    empresas = serializers.CharField(max_length=500)
    tiene_igv = serializers.BooleanField()
    descripcion = serializers.CharField(max_length=500)
    estado = serializers.CharField(max_length=10)
    fecha_actualizacion = serializers.DateField()
    clientesportales_id = serializers.IntegerField()
    clientesportales = serializers.CharField(max_length=500)

class ProductUpdateStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['estado']
