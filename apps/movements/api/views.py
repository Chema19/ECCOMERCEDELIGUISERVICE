from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.movements.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

class MovementCreateView(generics.CreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovementSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Movimiento()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_emisor_id = request.data['colaboradores_emisor']
        obj.colaboradores_transporte_id = request.data['colaboradores_transporte']
        obj.colaboradores_receptor_id = request.data['colaboradores_receptor']
        obj.tiendas_origen_id = request.data['tiendas_origen']
        obj.tiendas_destino_id = request.data['tiendas_destino']
        obj.fue_preparado = request.data['fue_preparado']
        obj.fue_enviado = request.data['fue_enviado']
        obj.fue_recibido = request.data['fue_recibido']
        obj.descripcion = request.data['descripcion']
        obj.fecha_movimiento = request.data['fecha_movimiento']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_movimientos = request.data['detalles_movimientos']
        obj.save()
        for item in lst_detalles_movimientos:
            obj_detalle_movimiento = DetalleMovimiento()
            obj_detalle_movimiento.cantidad = item['cantidad']
            obj_detalle_movimiento.productos_id = item['productos']
            obj_detalle_movimiento.movimientos_id = obj.id
            obj_detalle_movimiento.estado = 'ACT'
            obj_detalle_movimiento.save()

        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class MovementUpdateView(generics.UpdateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovementSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Movimiento.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_emisor_id = request.data['colaboradores_emisor']
        obj.colaboradores_transporte_id = request.data['colaboradores_transporte']
        obj.colaboradores_receptor_id = request.data['colaboradores_receptor']
        obj.tiendas_origen_id = request.data['tiendas_origen']
        obj.tiendas_destino_id = request.data['tiendas_destino']
        obj.descripcion = request.data['descripcion']
        obj.fecha_movimiento = request.data['fecha_movimiento']
        obj.fue_preparado = request.data['fue_preparado']
        obj.fue_enviado = request.data['fue_enviado']
        obj.fue_recibido = request.data['fue_recibido']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_movimientos = request.data['detalles_movimientos']
        obj.save()

        DetalleMovimiento.objects.filter(Q(movimientos__id=_id)).update(estado='INA')
        for item in lst_detalles_movimientos:
            _id_detalle_movimiento = item['id']
            if _id_detalle_movimiento is None:
                obj_detalle_movimiento = DetalleMovimiento()
                obj_detalle_movimiento.cantidad = item['cantidad']
                obj_detalle_movimiento.productos_id = item['productos']
                obj_detalle_movimiento.movimientos_id = obj.id
                obj_detalle_movimiento.estado = 'ACT'
                obj_detalle_movimiento.save()
                obj.save()
            else:
                obj_detalle_movimiento = DetalleMovimiento.objects.get(Q(id=_id_detalle_movimiento))
                obj_detalle_movimiento.cantidad = item['cantidad']
                obj_detalle_movimiento.productos_id = item['productos']
                obj_detalle_movimiento.movimientos_id = obj.id
                obj_detalle_movimiento.estado = 'ACT'
                obj_detalle_movimiento.save()
                obj.save()

        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class MovementListView(generics.ListAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovementListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tiendas_origen','codigo']

    def list(self, request, *args, **kwargs):
        movimiento = Movimiento.objects.filter(Q(estado="ACT")).order_by('-id').all()

        tiendas = request.query_params.get('tiendas_origen')

        codigo = request.query_params.get('codigo')

        if tiendas:
            movimiento = movimiento.filter(Q(tiendas_destino_id=tiendas) | Q(tiendas_origen_id=tiendas))
        if codigo:
            movimiento = movimiento.filter(codigo=codigo)

        movimientos_paginated = self.paginate_queryset(movimiento)

        objectos = []
        for item in movimientos_paginated:
            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'fue_preparado': item.fue_preparado,
                'fue_enviado': item.fue_enviado,
                'fue_recibido': item.fue_recibido,
                'tiendas_origen_id': item.tiendas_origen.id,
                'tiendas_origen': item.tiendas_origen.direccion,
                'tiendas_destino_id': item.tiendas_destino.id,
                'tiendas_destino': item.tiendas_destino.direccion,
                'descripcion': item.descripcion,
                'fecha_movimiento': item.fecha_movimiento,
                'estado': item.estado,
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
            objectos.append(objeto)

        serializer = MovementListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': movimiento.count(),
        }
        return Response(result)

class MovementDetailView(generics.RetrieveAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovementSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Movimiento.objects.get(Q(id=_id))

        detalles_movimientos = []
        for item_detalle_movimiento in DetalleMovimiento.objects.filter(Q(movimientos__id=_id) & Q(estado="ACT")):
            detalle_movimiento = {
                'id': item_detalle_movimiento.id,
                'cantidad': item_detalle_movimiento.cantidad,
                'productos': item_detalle_movimiento.productos_id,
                'movimientos': item_detalle_movimiento.movimientos_id,
                'estado': item_detalle_movimiento.estado
            }
            detalles_movimientos.append(detalle_movimiento)

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'colaboradores_emisor': value.colaboradores_emisor_id,
            'fue_preparado': value.fue_preparado,
            'colaboradores_transporte': value.colaboradores_transporte_id,
            'fue_enviado': value.fue_enviado,
            'colaboradores_receptor': value.colaboradores_receptor_id,
            'fue_recibido': value.fue_recibido,
            'tiendas_origen': value.tiendas_origen_id,
            'tiendas_destino': value.tiendas_destino_id,
            'descripcion': value.descripcion,
            'fecha_movimiento': value.fecha_movimiento,
            'detalles_movimientos': detalles_movimientos,
            'estado': value.estado,
            'clientesportales': value.clientesportales.nombre,
            'clientesportales_id': value.clientesportales.id,
        }

        serializer = MovementSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class MovementDeleteView(generics.DestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovementSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Movimiento.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        DetalleMovimiento.objects.filter(Q(estado="ACT") & Q(movimientos__id=_id)).update(estado="INA")
        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)
