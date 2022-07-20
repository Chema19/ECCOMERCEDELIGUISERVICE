from rest_framework import serializers
from apps.core.models import *


class DebtsPersonSerializer(serializers.Serializer):
    personas = serializers.IntegerField()
    personas_nombre = serializers.CharField(max_length=1000)
    credito = serializers.DecimalField(max_digits=15, decimal_places=2)

class CreditSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditoVenta
        fields = '__all__'

class CreditSaleListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    personas = serializers.CharField(max_length=500)
    personas_id = serializers.IntegerField()
    monto_pago = serializers.DecimalField(max_digits=15, decimal_places=2)
    fecha_abono = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    tiendas = serializers.CharField(max_length=500)
    tiendas_id = serializers.IntegerField()
    proveniencia = serializers.CharField(max_length=500)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()