from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from apps.core.models import *
from apps.deliveries.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from apps.core.constants import *
from decimal import *
from django_filters.rest_framework import DjangoFilterBackend

class DeliveryCreateView(generics.CreateAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Entrega()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_emisor_id = request.data['colaboradores_emisor']
        obj.colaboradores_transporte_id = request.data['colaboradores_transporte']
        obj.personas_id = request.data['personas']
        obj.tiendas_id = request.data['tiendas']
        obj.fue_preparado = request.data['fue_preparado']
        obj.fue_enviado = request.data['fue_enviado']
        obj.fue_entregado = request.data['fue_entregado']
        obj.descripcion = request.data['descripcion']
        obj.fecha_entrega = request.data['fecha_entrega']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_entregas = request.data['detalles_entregas']
        obj.save()
        for item in lst_detalles_entregas:
            obj_detalle_entrega = DetalleEntrega()
            obj_detalle_entrega.cantidad = item['cantidad']
            obj_detalle_entrega.productos_id = item['productos']
            obj_detalle_entrega.entregas_id = obj.id
            obj_detalle_entrega.estado = 'ACT'
            obj_detalle_entrega.save()

        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class DeliveryUpdateView(generics.UpdateAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliverySerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Entrega.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.colaboradores_emisor_id = request.data['colaboradores_emisor']
        obj.colaboradores_transporte_id = request.data['colaboradores_transporte']
        obj.tiendas_id = request.data['tiendas']
        obj.personas_id = request.data['personas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_entrega = request.data['fecha_entrega']
        obj.fue_preparado = request.data['fue_preparado']
        obj.fue_enviado = request.data['fue_enviado']
        obj.fue_entregado = request.data['fue_entregado']
        obj.clientesportales_id = request.data['clientesportales']

        lst_detalles_entregas = request.data['detalles_entregas']
        obj.save()

        DetalleEntrega.objects.filter(Q(entregas__id=_id)).update(estado='INA')
        for item in lst_detalles_entregas:
            _id_detalle_entrega = item['id']
            if _id_detalle_entrega is None:
                obj_detalle_entrega = DetalleEntrega()
                obj_detalle_entrega.cantidad = item['cantidad']
                obj_detalle_entrega.productos_id = item['productos']
                obj_detalle_entrega.entregas_id = obj.id
                obj_detalle_entrega.estado = 'ACT'
                obj_detalle_entrega.save()
                obj.save()
            else:
                obj_detalle_entrega = DetalleEntrega.objects.get(Q(id=_id_detalle_entrega))
                obj_detalle_entrega.cantidad = item['cantidad']
                obj_detalle_entrega.productos_id = item['productos']
                obj_detalle_entrega.entregas_id = obj.id
                obj_detalle_entrega.estado = 'ACT'
                obj_detalle_entrega.save()
                obj.save()

        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class DeliveryByCustomerListView(generics.ListAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliveryListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['personas__id']

    def list(self, request, *args, **kwargs):
        entrega = Entrega.objects.filter(Q(estado="ACT")).all()

        personas = request.query_params.get('personas__id')

        if personas:
            entrega = entrega.filter(Q(personas=personas))

        entrega_paginated = self.paginate_queryset(entrega)

        objectos = []
        for item in entrega_paginated:
           objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'fue_preparado': item.fue_preparado,
                'fue_enviado': item.fue_enviado,
                'fue_entregado': item.fue_entregado,
                'personas_id': item.personas.id,
                'personas': item.personas.clientes.nombres + " " + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'tiendas_id': item.tiendas_id,
                'tiendas': item.tiendas.direccion,
                'descripcion': item.descripcion,
                'fecha_entrega': item.fecha_entrega,
                'estado': item.estado,
                'proveniencia': 'Entrega' if item.ventas is None else 'Venta',
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
           objectos.append(objeto)

        serializer = DeliveryListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': entrega.count(),
        }
        return Response(result)

class DeliveryListView(generics.ListAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliveryListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo', 'fecha_entrega', 'tiendas__id', 'personas']

    def list(self, request, *args, **kwargs):
        personas = request.query_params.get('personas')
        tiendas = request.query_params.get('tiendas__id')
        fecha_entrega = request.query_params.get('fecha_entrega')
        codigo = request.query_params.get('codigo')

        entrega = Entrega.objects.filter(Q(estado="ACT")).order_by('-fecha_entrega')

        if personas:
            entrega = entrega.filter(Q(personas__clientes__nombres__icontains=personas) | Q(personas__clientes__apellidos__icontains=personas) | Q(personas__empresas__nombre_comercial__icontains=personas))
        if tiendas:
            entrega = entrega.filter(tiendas_id= tiendas)
        if fecha_entrega:
            entrega = entrega.filter(fecha_entrega=fecha_entrega)
        if codigo:
            entrega = entrega.filter(codigo=codigo)

        entrega_paginated = self.paginate_queryset(entrega)

        objectos = []
        for item in entrega_paginated:
           objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'fue_preparado': item.fue_preparado,
                'fue_enviado': item.fue_enviado,
                'fue_entregado': item.fue_entregado,
                'personas_id': item.personas.id,
                'personas': item.personas.clientes.nombres + " " + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'tiendas_id': item.tiendas_id,
                'tiendas': item.tiendas.direccion,
                'descripcion': item.descripcion,
                'fecha_entrega': item.fecha_entrega,
                'estado': item.estado,
                'proveniencia': 'Entrega' if item.ventas is None else 'Venta',
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales.id,
            }
           objectos.append(objeto)

        serializer = DeliveryListSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': entrega.count(),
        }
        return Response(result)

class DeliveryDetailView(generics.RetrieveAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Entrega.objects.get(Q(id=_id))

        detalles_entregas = []
        for item_detalle_entrega in DetalleEntrega.objects.filter(Q(entregas__id=_id) & Q(estado="ACT")):
            detalle_entrega = {
                'id': item_detalle_entrega.id,
                'cantidad': item_detalle_entrega.cantidad,
                'productos': item_detalle_entrega.productos_id,
                'entregas': item_detalle_entrega.entregas_id,
                'estado': item_detalle_entrega.estado
            }
            detalles_entregas.append(detalle_entrega)

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'colaboradores_emisor': value.colaboradores_emisor_id,
            'fue_preparado': value.fue_preparado,
            'colaboradores_transporte': value.colaboradores_transporte_id,
            'fue_enviado': value.fue_enviado,
            'personas': value.personas_id,
            'fue_entregado': value.fue_entregado,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_entrega': value.fecha_entrega,
            'detalles_entregas': detalles_entregas,
            'estado': value.estado,
            'clientesportales': value.clientesportales.id,
        }

        serializer = DeliverySerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class DeliveryDeleteView(generics.DestroyAPIView):
    queryset = Entrega.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Entrega.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        DetalleEntrega.objects.filter(Q(estado="ACT") & Q(entregas__id=_id)).update(estado="INA")
        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class ProductStockCustomerListView(generics.ListAPIView):
    queryset = Entrega.objects.all()
    serializer_class = StockCustomerSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filterset_fields = ['personas']

    def list(self, request, *args, **kwargs):

        personas = Persona.objects.filter(estado='ACT')
        nombre = request.query_params.get('personas')
        if nombre:
            personas = personas.filter(Q(clientes__nombres__icontains=nombre) |
                                       Q(clientes__apellidos__icontains=nombre) |
                                       Q(empresas__nombre_comercial__icontains=nombre))

        personas_paginated = self.paginate_queryset(personas)

        detalles_venta = DetalleVenta.objects.filter(estado="ACT",productos__estado="ACT")
        detalles_entrega = DetalleEntrega.objects.filter(estado="ACT",productos__estado="ACT")
        productos = Producto.objects.filter(estado="ACT")

        objectos = []
        for item in personas_paginated:
            detalles = []
            productos_comprados = list(detalles_venta.filter(ventas__personas_id=item.id).values_list('productos__id').distinct())
            productos_entregados = list(detalles_entrega.filter(entregas__personas_id=item.id).values_list('productos__id').distinct())
            union_productos = sorted(list(set(productos_comprados) | set(productos_entregados)))

            for item_producto in union_productos:

                sum_detalle_venta = detalles_venta.filter(productos_id=item_producto, ventas__personas_id=item.id).aggregate(Sum('cantidad'))['cantidad__sum']
                sum_detalle_entrega = detalles_entrega.filter(productos_id=item_producto, entregas__personas_id=item.id).aggregate(Sum('cantidad'))['cantidad__sum']
                producto = productos.get(id=item_producto[0])
                if (Decimal(sum_detalle_venta) if sum_detalle_venta is not None else 0) - (Decimal(sum_detalle_entrega) if sum_detalle_entrega is not None else 0) > 0:
                    detalle = {
                        'productos': producto.id,
                        'productos_nombre': producto.nombre,
                        'cantidad': (Decimal(sum_detalle_venta) if sum_detalle_venta is not None else 0) - (Decimal(sum_detalle_entrega) if sum_detalle_entrega is not None else 0)
                    }
                    detalles.append(detalle)

            objeto = {
                'personas': item.id,
                'personas_nombre': item.clientes.nombres + " " + item.clientes.apellidos if item.clientes_id is not None else item.empresas.nombre_comercial,
                'personas_documento': item.clientes.dni if item.clientes_id is not None else item.empresas.RUC,
                'personas_celular': item.clientes.celular if item.clientes_id is not None else item.empresas.celular,
                'detalles': detalles
            }
            objectos.append(objeto)

        serializer = StockCustomerSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': personas.count(),
        }
        return Response(result)