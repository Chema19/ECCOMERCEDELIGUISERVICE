from rest_framework import serializers
from apps.core.models import *

class ExpenseDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    monto_gastado = serializers.DecimalField(max_digits=6, decimal_places=2)
    productos_gastos = serializers.IntegerField()
    gastos = serializers.IntegerField()
    estado = serializers.CharField(max_length=10)

class ExpenseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    colaboradores = serializers.IntegerField()
    tiendas = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1000)
    fecha_gasto = serializers.DateField()
    detalles_gastos = ExpenseDetailSerializer(many=True)
    estado = serializers.CharField(max_length=10)
    clientesportales = serializers.IntegerField()



