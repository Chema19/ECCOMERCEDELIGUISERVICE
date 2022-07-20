from unicodedata import decimal

import django_filters
from django.db.models.functions import Upper
from rest_framework import generics, serializers, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.models import *
from apps.credits.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from apps.core.constants import *
from decimal import *

class DebtPersonListView(generics.ListAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = DebtsPersonSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination #StandardLimitOffSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['personas']

    def list(self, request, *args, **kwargs):
        personasfilter = request.query_params.get('personas')

        personas = Persona.objects.filter(Q(estado="ACT"))

        if personasfilter:
            personas = personas.filter(Q(clientes__nombres__icontains=personasfilter) | Q(clientes__apellidos__icontains=personasfilter) | Q(empresas__nombre_comercial__icontains=personasfilter))

        personas_paginated = self.paginate_queryset(personas)

        objectos = []
        for item in personas_paginated:
            ventas = Venta.objects.filter(Q(estado='ACT') & Q(personas_id=item.id)).aggregate(Sum('total'))['total__sum']
            pagos = CreditoVenta.objects.filter(Q(estado='ACT') & Q(personas_id=item.id)).aggregate(Sum('monto_pago'))['monto_pago__sum']
            objeto = {
                'personas': item.id,
                'personas_nombre': item.clientes.nombres + ' ' + item.clientes.apellidos if item.clientes_id is not None else item.empresas.nombre_comercial,
                'credito': (Decimal(ventas) if ventas is not None else 0) - (Decimal(pagos) if pagos is not None else 0)
            }
            objectos.append(objeto)

        serializer = DebtsPersonSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': personas.count(),
        }
        return Response(result)

class CreditSaleCreateView(generics.CreateAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = CreditoVenta()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.monto_pago = request.data['monto_pago']
        obj.fecha_abono = request.data['fecha_abono']
        obj.descripcion = request.data['descripcion']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.tipopagos_id = request.data['tipopagos']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class CreditSaleUpdateView(generics.UpdateAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = CreditoVenta.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.monto_pago = request.data['monto_pago']
        obj.fecha_abono = request.data['fecha_abono']
        obj.descripcion = request.data['descripcion']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.tipopagos_id = request.data['tipopagos']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class CreditSaleByCustomerListView(generics.ListAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination  # StandardLimitOffSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['colaboradores__id']

    def list(self, request, *args, **kwargs):
        customersfilter = request.query_params.get('colaboradores__id')

        creditosventas = CreditoVenta.objects.filter(Q(estado="ACT") & Q(personas_id=customersfilter))

        creditosventas_paginated = self.paginate_queryset(creditosventas)

        objectos = []
        for item in creditosventas_paginated:
            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'personas': item.personas.clientes.nombres + ' ' + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'personas_id': item.personas.id,
                'monto_pago': item.monto_pago,
                'fecha_abono': item.fecha_abono,
                'estado': item.estado,
                'tiendas': item.tiendas.direccion,
                'tiendas_id': item.tiendas.id,
                'proveniencia':  'Pago' if item.ventas is None else 'Venta',
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
            objectos.append(objeto)

        serializer = CreditSaleListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': creditosventas.count(),
        }
        return Response(result)

class CreditSaleListView(generics.ListAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo', 'fecha_abono', 'tiendas__id', 'personas']

    def list(self, request, *args, **kwargs):
        personas = request.query_params.get('personas')
        tiendas = request.query_params.get('tiendas__id')
        fecha_pago = request.query_params.get('fecha_abono')
        codigo = request.query_params.get('codigo')

        creditosventas = CreditoVenta.objects.filter(Q(estado="ACT")).order_by('-fecha_abono')

        if personas:
            creditosventas = creditosventas.filter(Q(personas__clientes__nombres__icontains=personas) | Q(personas__clientes__apellidos__icontains=personas) | Q(personas__empresas__nombre_comercial__icontains=personas))
        if tiendas:
            creditosventas = creditosventas.filter(tiendas_id= tiendas)
        if fecha_pago:
            creditosventas = creditosventas.filter(fecha_abono=fecha_pago)
        if codigo:
            creditosventas = creditosventas.filter(codigo=codigo)

        creditosventas_paginated = self.paginate_queryset(creditosventas)

        objectos = []
        for item in creditosventas_paginated:
            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'personas': item.personas.clientes.nombres + ' ' + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'personas_id': item.personas.id,
                'monto_pago': item.monto_pago,
                'fecha_abono': item.fecha_abono,
                'estado': item.estado,
                'tiendas': item.tiendas.direccion,
                'tiendas_id': item.tiendas.id,
                'proveniencia': 'Pago' if item.ventas is None else 'Venta',
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
            objectos.append(objeto)

        serializer = CreditSaleListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': creditosventas.count(),
        }
        return Response(result)

class CreditSaleDetailView(generics.RetrieveAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = CreditoVenta.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class CreditSaleDeleteView(generics.DestroyAPIView):
    queryset = CreditoVenta.objects.all()
    serializer_class = CreditSaleSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = CreditoVenta.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)