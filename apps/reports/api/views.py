from rest_framework import generics, serializers
from apps.core.models import *
from apps.reports.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.db import connection
from apps.core.constants import *
from rest_framework.permissions import *
from decimal import *
from django_filters.rest_framework import DjangoFilterBackend
import datetime

class CreditCustomerListView(generics.ListAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = CreditCustomerSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        personas = Persona.objects.filter(Q(estado="ACT"))
        objectos = []
        for item in personas:
            ventas = Venta.objects.filter(Q(estado='ACT') & Q(personas_id=item.id)).aggregate(Sum('total'))['total__sum']
            pagos = CreditoVenta.objects.filter(Q(estado='ACT') & Q(personas_id=item.id)).aggregate(Sum('monto_pago'))['monto_pago__sum']
            objeto = {
                'nombre': item.clientes.nombres + ' ' + item.clientes.apellidos if item.clientes_id is not None else item.empresas.nombre_comercial,
                'deuda': (Decimal(ventas) if ventas is not None else 0) - (Decimal(pagos) if pagos is not None else 0)
            }
            objectos.append(objeto)

        serializer = CreditCustomerSerializer(objectos, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SalesByDayReportView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleByDayReportSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fecha_venta']

    def list(self, request, *args, **kwargs):
        fecha_venta = request.query_params.get('fecha_venta')

        c = connection.cursor()
        date_time_obj = datetime.datetime.strptime(fecha_venta, '%Y-%m-%d')
        date = date_time_obj.date()
        c.callproc('get_sales', (date,))
        ventas = c.fetchall()
        c.close()

        ventas_json = []
        for venta_item in ventas:
            venta_detalle_json = []
            #detalles_ventas = DetalleVenta.objects.filter(estado='ACT',ventas__id=venta_item[0]).all()
            cdv = connection.cursor()
            cdv.callproc('get_sales_details', (venta_item[0],))
            detalles_ventas = cdv.fetchall()
            cdv.close()

            for venta_detalle_item in detalles_ventas:
                venta_detalle = {
                    'producto': venta_detalle_item[1],
                    'cantidad': venta_detalle_item[2],
                    'precio': venta_detalle_item[3],
                    'precio_total': venta_detalle_item[4]
                }
                venta_detalle_json.append(venta_detalle)

            venta = {
                'codigo': venta_item[1],
                'fecha_venta': venta_item[2],
                'tipo_pago': venta_item[3],
                'tipo_estado_producto': venta_item[4],
                'tipo_moneda': venta_item[5],
                'tienda': venta_item[6],
                'cliente': venta_item[7],
                'trabajador': venta_item[8],
                'total': venta_item[9],
                'sale_detail': venta_detalle_json
            }
            ventas_json.append(venta)

        serializer = SaleByDayReportSerializer(ventas_json, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class StockProductByStoreReportView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = StockProductByStoreReportSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        c = connection.cursor()
        c.callproc('get_stock_product_by_store', ())
        productostock = c.fetchall()
        c.close()

        objects_json = []
        for item in productostock:
            object = {
                'producto': item[0],
                'empresa': item[1],
                'tienda': item[2],
                'tiendaid': item[3],
                'entrega': item[4] if item[4] != None else 0,
                'movimientoentrada': item[5] if item[5] != None else 0,
                'movimientosalida': item[6] if item[6] != None else 0,
                'compra': item[7] if item[7] != None else 0,
            }
            objects_json.append(object)

        serializer = StockProductByStoreReportSerializer(objects_json, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SalePurchaseMovementsByStoreReportView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = StockProductByStoreReportSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tiendas_id']

    def list(self, request, *args, **kwargs):
        tiendas_id = request.query_params.get('tiendas_id')

        c = connection.cursor()
        c.callproc('get_entrada_compra_msalida_mentrada_by_store', (tiendas_id))
        sp_result = c.fetchall()
        c.close()

        objects_json = []
        for item in sp_result:
            object = {
                'tipo': item[0],
                'id': item[1],
                'codigo': item[2],
                'tienda': item[3],
                'tiendaid': item[4],
                'fecha': item[5],
                'producto': item[6],
                'productoid': item[7],
                'cantidad': item[8],
            }
            objects_json.append(object)

        serializer = SalePurchaseMovementsByStoreReportSerializer(objects_json, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

#EXCELES PARA LA HOMOLOGACION DE PRODUCTOS

class ProductsByBrandReportView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductByBrandReportSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        products = Producto.objects.filter(estado='ACT')
        objects_json = []
        for item in products:
            object = {
                'id' : item.id,
                'nombre' : item.nombre,
                'empresa_id' : item.empresas.id if item.empresas_id is not None else None,
                'empresa' : item.empresas.razon_social if item.empresas_id is not None else "-",
                'nombre_comercial' : item.empresas.nombre_comercial if item.empresas_id is not None else "-"
            }
            objects_json.append(object)


        serializer = ProductByBrandReportSerializer(objects_json, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)