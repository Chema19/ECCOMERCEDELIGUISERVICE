from rest_framework import generics, serializers
from apps.core.models import *
from apps.typesusers.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from apps.core.constants import *
from rest_framework.permissions import *

class StockProductoUploadView(generics.CreateAPIView):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = Compra()
        obj.estado = 'ACT'
        obj.codigo = 'CARGAMASIVA'
        obj.personas_id = 3
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = '-'
        obj.fecha_compra = request.data['fecha']
        obj.tipomonedas_id = 1

        lst_detalles_compras = request.data['stock_productos_detalles']
        obj.save()
        for item in lst_detalles_compras:
            _id_producto = item['id']
            _precio_original_producto = Producto.objects.get(Q(id=_id_producto)).precio_base

            obj_detalle_compra = DetalleCompra()
            obj_detalle_compra.precio_unitario = 0
            obj_detalle_compra.precio_sin_descuento = 0
            obj_detalle_compra.cantidad = item['cantidad_tienda'] - item['cantidad']
            obj_detalle_compra.total = 0
            obj_detalle_compra.productos_id = item['id']
            obj_detalle_compra.compras_id = obj.id
            obj_detalle_compra.estado = 'ACT'
            obj_detalle_compra.save()

        obj.total = DetalleCompra.objects.filter(Q(estado="ACT") & Q(compras__id=obj.id)).aggregate(Sum('total'))['total__sum']
        _total = obj.total
        obj.impuesto = ((float(_total) * 18.00) / 100.00)
        obj.save()

        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)



