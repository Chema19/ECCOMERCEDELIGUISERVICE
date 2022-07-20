from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.expenses.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from apps.core.constants import *
from decimal import *

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Gasto.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Gasto()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_gasto = request.data['fecha_gasto']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_gastos = request.data['detalles_gastos']
        obj.save()
        for item in lst_detalles_gastos:
            obj_detalle_gasto = DetalleGasto()
            obj_detalle_gasto.monto_gastado = item['monto_gastado']
            obj_detalle_gasto.productos_gastos_id = item['productos_gastos']
            obj_detalle_gasto.gastos_id = obj.id
            obj_detalle_gasto.estado = 'ACT'
            obj_detalle_gasto.save()

        obj.total = DetalleGasto.objects.filter(Q(estado="ACT") & Q(gastos__id=obj.id)).aggregate(Sum('monto_gastado'))['monto_gastado__sum']
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

class ExpenseUpdateView(generics.UpdateAPIView):
    queryset = Gasto.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Gasto.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_gasto = request.data['fecha_gasto']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_gastos = request.data['detalles_gastos']
        obj.save()

        DetalleGasto.objects.filter(Q(gastos__id=_id)).update(estado='INA')
        for item in lst_detalles_gastos:
            _id_detalle_gasto = item['id']
            if _id_detalle_gasto is None:
                obj_detalle_gasto = DetalleGasto()
                obj_detalle_gasto.monto_gastado = item['monto_gastado']
                obj_detalle_gasto.productos_gastos_id = item['productos_gastos']
                obj_detalle_gasto.gastos_id = obj.id
                obj_detalle_gasto.estado = 'ACT'
                obj_detalle_gasto.save()
                obj.save()
            else:
                obj_detalle_gasto = DetalleGasto.objects.get(Q(id=_id_detalle_gasto))
                obj_detalle_gasto.monto_gastado = item['monto_gastado']
                obj_detalle_gasto.productos_gastos_id = item['productos_gastos']
                obj_detalle_gasto.gastos_id = obj.id
                obj_detalle_gasto.estado = 'ACT'
                obj_detalle_gasto.save()
                obj.save()

        obj.total = DetalleGasto.objects.filter(Q(estado="ACT") & Q(gastos__id=obj.id)).aggregate(Sum('monto_gastado'))['monto_gastado__sum']
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

class ExpenseListView(generics.ListAPIView):
    queryset = Gasto.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        value = Gasto.objects.filter(Q(estado="ACT")).all()
        objectos = []
        for item in value:
            detalles_gastos = []
            for item_detalle_gasto in DetalleGasto.objects.filter(Q(estado="ACT") & Q(gastos__id=item.id)):
                detalle_gasto = {
                    'id': item_detalle_gasto.id,
                    'monto_gastado': item_detalle_gasto.monto_gastado,
                    'productos_gastos': item_detalle_gasto.productos_gastos_id,
                    'gastos': item_detalle_gasto.gastos_id,
                    'estado': item_detalle_gasto.estado
                }
                detalles_gastos.append(detalle_gasto)

            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'colaboradores': item.colaboradores_id,
                'tiendas': item.tiendas_id,
                'descripcion': item.descripcion,
                'fecha_gasto': item.fecha_gasto,
                'detalles_gastos': detalles_gastos,
                'estado': item.estado,
                'clientesportales': item.clientesportales_id
            }
            objectos.append(objeto)

        serializer = ExpenseSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class ExpenseDetailView(generics.RetrieveAPIView):
    queryset = Gasto.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Gasto.objects.get(Q(id=_id))

        detalles_gastos = []
        for item_detalle_gasto in DetalleGasto.objects.filter(Q(gastos__id=_id) & Q(estado="ACT")):
            detalle_gasto = {
                'id': item_detalle_gasto.id,
                'monto_gastado': item_detalle_gasto.monto_gastado,
                'productos_gastos': item_detalle_gasto.productos_gastos_id,
                'gastos': item_detalle_gasto.gastos_id,
                'estado': item_detalle_gasto.estado
            }
            detalles_gastos.append(detalle_gasto)

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'colaboradores': value.colaboradores_id,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_gasto': value.fecha_gasto,
            'detalles_gastos': detalles_gastos,
            'estado': value.estado,
            'clientesportales': value.clientesportales_id
        }

        serializer = ExpenseSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class ExpenseDeleteView(generics.DestroyAPIView):
    queryset = Gasto.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Gasto.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        DetalleGasto.objects.filter(Q(estado="ACT") & Q(gastos__id=_id)).update(estado="INA")
        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

