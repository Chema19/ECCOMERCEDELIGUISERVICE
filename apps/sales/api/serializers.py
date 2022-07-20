from rest_framework import serializers
from apps.core.models import *

class SaleDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    precio_sin_descuento = serializers.DecimalField(max_digits=15, decimal_places=2)
    precio_unitario = serializers.DecimalField(max_digits=15, decimal_places=2)
    cantidad = serializers.DecimalField(max_digits=15, decimal_places=2)
    descuento_unitario = serializers.DecimalField(max_digits=15, decimal_places=2)
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    productos = serializers.IntegerField()
    ventas = serializers.IntegerField()
    estado = serializers.CharField(max_length=10)

class SaleCreditBoletaFacturaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    monto_pagar = serializers.DecimalField(max_digits=15, decimal_places=2)
    fecha_pagar = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    ventas = serializers.IntegerField()

class SaleApprovalVoucherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    comprobanteaprobado = serializers.CharField(max_length=500)

class SaleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    personas = serializers.IntegerField()
    colaboradores = serializers.IntegerField()
    tiendas = serializers.IntegerField()
    descripcion = serializers.CharField(max_length=1000)
    fecha_venta = serializers.DateField()
    detalles_ventas = SaleDetailSerializer(many=True)
    sales_credits_boletafactura = SaleCreditBoletaFacturaSerializer(many=True)
    estado = serializers.CharField(max_length=10)
    tipopagos = serializers.IntegerField()
    tipoestadoproductos = serializers.IntegerField()
    tipomonedas = serializers.IntegerField()
    monto_pago = serializers.DecimalField(max_digits=15, decimal_places=2)
    tipocomprobante_factura = serializers.CharField(max_length=500)
    tipoigv_factura = serializers.CharField(max_length=500)
    tipopago_factura = serializers.CharField(max_length=500)
    clientesportales = serializers.IntegerField()
    comprobanteaprobado = serializers.CharField(max_length=500)

class SaleListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    codigo = serializers.CharField(max_length=500)
    personas = serializers.CharField(max_length=500)
    personas_id = serializers.IntegerField()
    tiendas = serializers.CharField(max_length=500)
    tiendas_id = serializers.IntegerField()
    fecha_venta = serializers.DateField()
    estado = serializers.CharField(max_length=10)
    tipo_pago = serializers.CharField(max_length=500)
    tipo_estado_producto = serializers.CharField(max_length=500)
    tipo_moneda = serializers.CharField(max_length=500)
    tipocomprobante_factura = serializers.CharField(max_length=500)
    tipoigv_factura = serializers.CharField(max_length=500)
    tipopago_factura = serializers.CharField(max_length=500)
    clientesportales = serializers.CharField(max_length=500)
    clientesportales_id = serializers.IntegerField()
    comprobanteaprobado = serializers.CharField(max_length=500)