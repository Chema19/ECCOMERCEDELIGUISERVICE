from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.purchases.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.constants import *

class PurchaseCreateView(generics.CreateAPIView):
    queryset = Compra.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Compra()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_compra = request.data['fecha_compra']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_compras = request.data['detalles_compras']
        obj.save()
        for item in lst_detalles_compras:
            _id_producto = item['productos']
            _precio_original_producto = Producto.objects.get(Q(id=_id_producto)).precio_base

            obj_detalle_compra = DetalleCompra()
            obj_detalle_compra.precio_unitario = item['precio_unitario']
            obj_detalle_compra.precio_sin_descuento = _precio_original_producto
            obj_detalle_compra.cantidad = item['cantidad']
            obj_detalle_compra.total = item['cantidad'] * item['precio_unitario']
            obj_detalle_compra.productos_id = item['productos']
            obj_detalle_compra.compras_id = obj.id
            obj_detalle_compra.cambiar_precio = item['cambiar_precio']
            obj_detalle_compra.precio_unitario_compra = item['precio_unitario_compra']
            obj_detalle_compra.tipo_cambio = item['tipo_cambio']
            obj_detalle_compra.porcentaje_ganancia = item['porcentaje_ganancia']
            obj_detalle_compra.precio_unitario_soles = item['precio_unitario_soles']
            obj_detalle_compra.precio_venta = item['precio_venta']

            obj_detalle_compra.estado = 'ACT'
            obj_detalle_compra.save()

            if obj_detalle_compra.cambiar_precio == True:
                cambiar_precio_producto = Producto.objects.get(id=_id_producto)
                cambiar_precio_producto.precio_base = item['precio_venta']
                cambiar_precio_producto.save()

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

class PurchaseUpdateView(generics.UpdateAPIView):
    queryset = Compra.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Compra.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_compra = request.data['fecha_compra']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_compras = request.data['detalles_compras']
        obj.save()

        DetalleCompra.objects.filter(Q(compras__id=_id)).update(estado='INA')
        for item in lst_detalles_compras:
            _id_producto = item['productos']
            _precio_original_producto = Producto.objects.get(Q(id=_id_producto)).precio_base
            _id_detalle_compra = item['id']
            if _id_detalle_compra is None:
                obj_detalle_compra = DetalleCompra()
                obj_detalle_compra.precio_unitario = item['precio_unitario']
                obj_detalle_compra.precio_sin_descuento = _precio_original_producto
                obj_detalle_compra.cantidad = item['cantidad']
                obj_detalle_compra.total = item['cantidad'] * item['precio_unitario']
                obj_detalle_compra.productos_id = item['productos']
                obj_detalle_compra.compras_id = obj.id

                obj_detalle_compra.cambiar_precio = item['cambiar_precio']
                obj_detalle_compra.precio_unitario_compra = item['precio_unitario_compra']
                obj_detalle_compra.tipo_cambio = item['tipo_cambio']
                obj_detalle_compra.porcentaje_ganancia = item['porcentaje_ganancia']
                obj_detalle_compra.precio_unitario_soles = item['precio_unitario_soles']
                obj_detalle_compra.precio_venta = item['precio_venta']

                obj_detalle_compra.estado = 'ACT'
                obj_detalle_compra.save()

                if obj_detalle_compra.cambiar_precio == True:
                    cambiar_precio_producto = Producto.objects.get(id=_id_producto)
                    cambiar_precio_producto.precio_base = item['precio_venta']
                    cambiar_precio_producto.save()

                obj.save()
            else:

                obj_detalle_compra = DetalleCompra.objects.get(Q(id=_id_detalle_compra))
                obj_detalle_compra.precio_unitario = item['precio_unitario']
                obj_detalle_compra.precio_sin_descuento = _precio_original_producto
                obj_detalle_compra.cantidad = item['cantidad']
                obj_detalle_compra.total = item['cantidad'] * item['precio_unitario']
                obj_detalle_compra.productos_id = item['productos']
                obj_detalle_compra.compras_id = obj.id

                obj_detalle_compra.cambiar_precio = item['cambiar_precio']
                obj_detalle_compra.precio_unitario_compra = item['precio_unitario_compra']
                obj_detalle_compra.tipo_cambio = item['tipo_cambio']
                obj_detalle_compra.porcentaje_ganancia = item['porcentaje_ganancia']
                obj_detalle_compra.precio_unitario_soles = item['precio_unitario_soles']
                obj_detalle_compra.precio_venta = item['precio_venta']

                obj_detalle_compra.estado = 'ACT'
                obj_detalle_compra.save()

                if obj_detalle_compra.cambiar_precio == True:
                    cambiar_precio_producto = Producto.objects.get(id=_id_producto)
                    cambiar_precio_producto.precio_base = item['precio_venta']
                    cambiar_precio_producto.save()

                obj.save()

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

class PurchaseListView(generics.ListAPIView):
    queryset = Compra.objects.all()
    serializer_class = PurchaseListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo', 'fecha_compra', 'tiendas__id', 'personas']


    def list(self, request, *args, **kwargs):

        personas = request.query_params.get('personas')
        tiendas = request.query_params.get('tiendas__id')
        fecha_compra = request.query_params.get('fecha_compra')
        codigo = request.query_params.get('codigo')

        compras = Compra.objects.filter(Q(estado="ACT")).order_by('-id').all()

        if personas:
            compras = compras.filter(Q(personas__clientes__nombres__icontains=personas) | Q(
                personas__clientes__apellidos__icontains=personas) | Q(
                personas__empresas__nombre_comercial__icontains=personas))
        if tiendas:
            compras = compras.filter(tiendas_id=tiendas)
        if fecha_compra:
            compras = compras.filter(fecha_compra=fecha_compra)
        if codigo:
            compras = compras.filter(codigo=codigo)

        compras_paginated = self.paginate_queryset(compras)

        objectos = []
        for item in compras_paginated:
            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'tiendas': item.tiendas.direccion,
                'tiendas_id': item.tiendas.id,
                'personas': item.personas.clientes.nombres + " " + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'personas_id': item.personas.id,
                'fecha_compra': item.fecha_compra,
                'estado': item.estado,
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
            objectos.append(objeto)

        serializer = PurchaseListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': compras.count(),
        }
        return Response(result)

class PurchaseDetailView(generics.RetrieveAPIView):
    queryset = Compra.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Compra.objects.get(Q(id=_id))

        detalles_compras = []
        for item_detalle_compra in DetalleCompra.objects.filter(Q(compras__id=_id) & Q(estado="ACT")):
            detalle_compra = {
                'id': item_detalle_compra.id,
                'precio_unitario': item_detalle_compra.precio_unitario,
                'cantidad': item_detalle_compra.cantidad,
                'productos': item_detalle_compra.productos_id,
                'compras': item_detalle_compra.compras_id,
                'total': item_detalle_compra.total,
                'cambiar_precio': item_detalle_compra.cambiar_precio,
                'precio_unitario_compra': item_detalle_compra.precio_unitario_compra,
                'tipo_cambio': item_detalle_compra.tipo_cambio,
                'porcentaje_ganancia': item_detalle_compra.porcentaje_ganancia,
                'precio_unitario_soles': item_detalle_compra.precio_unitario_soles,
                'precio_venta': item_detalle_compra.precio_venta,
                'estado': item_detalle_compra.estado
            }
            detalles_compras.append(detalle_compra)

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'personas': value.personas_id,
            'colaboradores': value.colaboradores_id,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_compra': value.fecha_compra,
            'tipomonedas': value.tipomonedas_id,
            'detalles_compras': detalles_compras,
            'estado': value.estado,
            'clientesportales': value.clientesportales.nombre,
            'clientesportales_id': value.clientesportales.id,
        }

        serializer = PurchaseSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class PurchaseDeleteView(generics.DestroyAPIView):
    queryset = Compra.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Compra.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        DetalleCompra.objects.filter(Q(estado="ACT") & Q(compras__id=_id)).update(estado="INA")
        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)
