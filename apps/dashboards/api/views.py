from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.dashboards.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum, F
from apps.core.constants import *
import datetime
from decimal import *
from django_filters.rest_framework import DjangoFilterBackend

class SaleAmountSolesByLocalAndDailyDataView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = DecimalValueSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        current_date = datetime.datetime.now()

        valortotal = Venta.objects.filter(Q(estado="ACT") &
                                          Q(tiendas__id=_id_local) &
                                          Q(fecha_venta__day=current_date.day) &
                                          Q(fecha_venta__month=current_date.month) &
                                          Q(fecha_venta__year=current_date.year) &
                                          Q(tipomonedas_id=1)).aggregate(Sum('total'))['total__sum']

        valorcredito = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tipopagos_id=2) &
                                            Q(tiendas__id=_id_local) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=1)).aggregate(Sum('total'))['total__sum']

        valorcontado = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tipopagos_id=1) &
                                            Q(tiendas__id=_id_local) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=1)).aggregate(Sum('total'))['total__sum']

        valortransferencia = Venta.objects.filter(Q(estado="ACT") &
                                                  Q(tipopagos_id=6) &
                                                  Q(tiendas__id=_id_local) &
                                                  Q(fecha_venta__day=current_date.day) &
                                                  Q(fecha_venta__month=current_date.month) &
                                                  Q(fecha_venta__year=current_date.year) &
                                                  Q(tipomonedas_id=1)).aggregate(Sum('total'))['total__sum']

        valoramortizacion = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                        ~Q(ventas__id=None) &
                                                        Q(tiendas__id=_id_local) &
                                                        Q(fecha_abono__day=current_date.day) &
                                                        Q(fecha_abono__month=current_date.month) &
                                                        Q(fecha_abono__year=current_date.year) &
                                                        Q(tipopagos_id=3) &
                                                        Q(tipomonedas_id=1)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        valorcreditoamortizacioncontado = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                      Q(ventas__id=None) &
                                                      Q(tiendas__id=_id_local) &
                                                      Q(fecha_abono__day=current_date.day) &
                                                      Q(fecha_abono__month=current_date.month) &
                                                      Q(fecha_abono__year=current_date.year) &
                                                      Q(tipopagos_id=1) &
                                                      Q(tipomonedas_id=1)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        valorcreditoamortizaciontransaccion = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                      Q(ventas__id=None) &
                                                      Q(tiendas__id=_id_local) &
                                                      Q(fecha_abono__day=current_date.day) &
                                                      Q(fecha_abono__month=current_date.month) &
                                                      Q(fecha_abono__year=current_date.year) &
                                                      Q(tipopagos_id=6) &
                                                      Q(tipomonedas_id=1)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        objeto = {
            'valortotal': valortotal,
            'valorcredito': valorcredito,
            'valorcontado': valorcontado,
            'valortransferencia': valortransferencia,
            'valoramortizacion': valoramortizacion,
            'valorcreditoamortizacioncontado': valorcreditoamortizacioncontado,
            'valorcreditoamortizaciontransaccion': valorcreditoamortizaciontransaccion
        }
        serializer = DecimalValueSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleCountSolesByLocalAndDailyDataView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = IntegerValueSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        current_date = datetime.datetime.now()
        valuetotal = Venta.objects.filter(Q(estado="ACT") &
                                          Q(tiendas__id=_id_local) &
                                          Q(fecha_venta__day=current_date.day) &
                                          Q(fecha_venta__month=current_date.month) &
                                          Q(fecha_venta__year=current_date.year) &
                                          Q(tipomonedas_id=1)).count()
        valuecredito = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tiendas__id=_id_local) &
                                            Q(tipopagos_id=2) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=1)).count()
        valuecontado = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tiendas__id=_id_local) &
                                            Q(tipopagos_id=1) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=1)).count()
        #valueamortizacion = Venta.objects.filter(Q(estado="ACT") &
        #                                         Q(tiendas__id=_id_local) &
        #                                         Q(tipopagos_id=3) &
        #                                         Q(fecha_venta__day=current_date.day) &
        #                                         Q(fecha_venta__month=current_date.month) &
        #                                         Q(fecha_venta__year=current_date.year) &
        #                                         Q(tipomonedas_id=1)).count()

        valueamortizacion = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                        ~Q(ventas__id=None) &
                                                        Q(tiendas__id=_id_local) &
                                                        Q(fecha_abono__day=current_date.day) &
                                                        Q(fecha_abono__month=current_date.month) &
                                                        Q(fecha_abono__year=current_date.year) &
                                                        Q(tipopagos_id=3) &
                                                        Q(tipomonedas_id=1)).count()

        valuetransferencia = Venta.objects.filter(Q(estado="ACT") &
                                                  Q(tiendas__id=_id_local) &
                                                  Q(tipopagos_id=6) &
                                                  Q(fecha_venta__day=current_date.day) &
                                                  Q(fecha_venta__month=current_date.month) &
                                                  Q(fecha_venta__year=current_date.year) &
                                                  Q(tipomonedas_id=1)).count()
        valueanulados = Venta.objects.filter(Q(estado="ACT") &
                                             Q(tiendas__id=_id_local) &
                                             Q(tipopagos_id=5) &
                                             Q(fecha_venta__day=current_date.day) &
                                             Q(fecha_venta__month=current_date.month) &
                                             Q(fecha_venta__year=current_date.year) &
                                             Q(tipomonedas_id=1)).count()
        objeto = {
            'valortotal': valuetotal,
            'valorcredito': valuecredito,
            'valorcontado': valuecontado,
            'valoramortizacion': valueamortizacion,
            'valortransferencia': valuetransferencia,
            'valoranulados': valueanulados,
        }
        serializer = IntegerValueSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleAmountDolaresByLocalAndDailyDataView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = DecimalValueSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        current_date = datetime.datetime.now()
        valortotal = Venta.objects.filter(Q(estado="ACT") &
                                          Q(tiendas__id=_id_local) &
                                          Q(fecha_venta__day=current_date.day) &
                                          Q(fecha_venta__month=current_date.month) &
                                          Q(fecha_venta__year=current_date.year) &
                                          Q(tipomonedas_id=2)).aggregate(Sum('total'))['total__sum']
        valorventacredito = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tipopagos_id=2) &
                                            Q(tiendas__id=_id_local) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=2)).aggregate(Sum('total'))['total__sum']
        valorventacontado = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tipopagos_id=1) &
                                            Q(tiendas__id=_id_local) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=2)).aggregate(Sum('total'))['total__sum']
        valorventatransferencia = Venta.objects.filter(Q(estado="ACT") &
                                                  Q(tipopagos_id=6) &
                                                  Q(tiendas__id=_id_local) &
                                                  Q(fecha_venta__day=current_date.day) &
                                                  Q(fecha_venta__month=current_date.month) &
                                                  Q(fecha_venta__year=current_date.year) &
                                                  Q(tipomonedas_id=2)).aggregate(Sum('total'))['total__sum']
        #valorventaamortizacion = Venta.objects.filter(Q(estado="ACT") &
        #                                         Q(tipopagos_id=3) &
        #                                         Q(tiendas__id=_id_local) &
        #                                         Q(fecha_venta__day=current_date.day) &
        #                                         Q(fecha_venta__month=current_date.month) &
        #                                         Q(fecha_venta__year=current_date.year) &
        #                                         Q(tipomonedas_id=2)).aggregate(Sum('total'))['total__sum']

        valorventaamortizacion = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                        ~Q(ventas__id=None) &
                                                        Q(tiendas__id=_id_local) &
                                                        Q(fecha_abono__day=current_date.day) &
                                                        Q(fecha_abono__month=current_date.month) &
                                                        Q(fecha_abono__year=current_date.year) &
                                                        Q(tipopagos_id=3) &
                                                        Q(tipomonedas_id=2)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        valorcreditoamortizacioncontado = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                      Q(ventas__id=None) &
                                                      Q(tiendas__id=_id_local) &
                                                      Q(fecha_abono__day=current_date.day) &
                                                      Q(fecha_abono__month=current_date.month) &
                                                      Q(fecha_abono__year=current_date.year) &
                                                      Q(tipopagos_id=1)&
                                                      Q(tipomonedas_id=2)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        valorcreditoamortizaciontransaccion = CreditoVenta.objects.filter(Q(estado="ACT") &
                                                      Q(ventas__id=None) &
                                                      Q(tiendas__id=_id_local) &
                                                      Q(fecha_abono__day=current_date.day) &
                                                      Q(fecha_abono__month=current_date.month) &
                                                      Q(fecha_abono__year=current_date.year) &
                                                      Q(tipopagos_id=6)&
                                                      Q(tipomonedas_id=2)).aggregate(Sum('monto_pago'))['monto_pago__sum']

        objeto = {
            'valortotal': valortotal,
            'valorcredito': valorventacredito,
            'valorcontado': valorventacontado,
            'valortransferencia': valorventatransferencia,
            'valoramortizacion': valorventaamortizacion,
            'valorcreditoamortizacioncontado': valorcreditoamortizacioncontado,
            'valorcreditoamortizaciontransaccion': valorcreditoamortizaciontransaccion
        }
        serializer = DecimalValueSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleCountDolaresByLocalAndDailyDataView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = IntegerValueSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        current_date = datetime.datetime.now()
        valuetotal = Venta.objects.filter(Q(estado="ACT") &
                                          Q(tiendas__id=_id_local) &
                                          Q(fecha_venta__day=current_date.day) &
                                          Q(fecha_venta__month=current_date.month) &
                                          Q(fecha_venta__year=current_date.year) &
                                          Q(tipomonedas_id=2)).count()
        valuecredito = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tiendas__id=_id_local) &
                                            Q(tipopagos_id=2) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=2)).count()
        valuecontado = Venta.objects.filter(Q(estado="ACT") &
                                            Q(tiendas__id=_id_local) &
                                            Q(tipopagos_id=1) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year) &
                                            Q(tipomonedas_id=2)).count()
        valueamortizacion = Venta.objects.filter(Q(estado="ACT") &
                                                 Q(tiendas__id=_id_local) &
                                                 Q(tipopagos_id=3) &
                                                 Q(fecha_venta__day=current_date.day) &
                                                 Q(fecha_venta__month=current_date.month) &
                                                 Q(fecha_venta__year=current_date.year) &
                                                 Q(tipomonedas_id=2)).count()
        valuetransferencia = Venta.objects.filter(Q(estado="ACT") & Q(tiendas__id=_id_local) &
                                                  Q(tipopagos_id=6) &
                                                  Q(fecha_venta__day=current_date.day) &
                                                  Q(fecha_venta__month=current_date.month) &
                                                  Q(fecha_venta__year=current_date.year) &
                                                  Q(tipomonedas_id=2)).count()
        valueanulados = Venta.objects.filter(Q(estado="ACT") &
                                             Q(tiendas__id=_id_local) &
                                             Q(tipopagos_id=5) &
                                             Q(fecha_venta__day=current_date.day) &
                                             Q(fecha_venta__month=current_date.month) &
                                             Q(fecha_venta__year=current_date.year) &
                                             Q(tipomonedas_id=2)).count()
        objeto = {
            'valortotal': valuetotal,
            'valorcredito': valuecredito,
            'valorcontado': valuecontado,
            'valoramortizacion': valueamortizacion,
            'valortransferencia': valuetransferencia,
            'valoranulados': valueanulados,
        }

        serializer = IntegerValueSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleCountByLocalAndMonthListView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleCountByLocalSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        current_date = datetime.datetime.now()
        list = []
        for item in Tienda.objects.filter(Q(estado="ACT")):
            conteos = []
            for item_2 in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                conteo = {
                    'mes': item_2,
                    'cantidad': Venta.objects.filter(Q(estado="ACT") & Q(tiendas__id=item.id) & Q(fecha_venta__month=item_2) & Q(fecha_venta__year=current_date.year)).count()
                }
                conteos.append(conteo)
            objeto = {
                'tiendas': item.id,
                'nombre_tienda': item.direccion,
                'cantidades': conteos
            }
            list.append(objeto)
        serializer = SaleCountByLocalSerializer(list, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleAmonthByLocalAndMonthListView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleAmountByLocalSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        current_date = datetime.datetime.now()
        list = []
        for item in Tienda.objects.filter(Q(estado="ACT")):
            conteos = []
            for item_2 in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                conteo = {
                    'mes': item_2,
                    'cantidad': DetalleVenta.objects.filter(Q(estado="ACT") &
                                                            Q(ventas__tiendas__id=item.id) &
                                                            Q(ventas__fecha_venta__month=item_2) &
                                                            Q(ventas__fecha_venta__year=current_date.year)).aggregate(Sum('total'))['total__sum'],
                }
                conteos.append(conteo)
            objeto = {
                'tiendas': item.id,
                'nombre_tienda': item.direccion,
                'cantidades': conteos
            }
            list.append(objeto)
        serializer = SaleAmountByLocalSerializer(list, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class StockProductByLocalListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = StockProductSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre']

    def list(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']

        productos = Producto.objects.filter(estado="ACT").order_by('nombre')

        nombre = request.query_params.get('nombre')
        if nombre:
            productos = productos.filter(Q(nombre__icontains=nombre))

        productos = productos.all()[:10]

        detalle_movimiento = DetalleMovimiento.objects.filter(estado="ACT").all()
        detalle_compra = DetalleCompra.objects.filter(estado="ACT").all()
        detalle_entrega = DetalleEntrega.objects.filter(estado="ACT").all()
        list = []
        for item in productos:
            # SALIDA DE PRODUCTO
            producto_movimiento_salida = detalle_movimiento.filter(Q(estado="ACT") &
                                                                           Q(movimientos__tiendas_origen_id=_id_local) &
                                                                           Q(productos__id=item.id) &
                                                                           Q(movimientos__fue_recibido=True)).aggregate(Sum('cantidad'))['cantidad__sum']
            #  ENTRADA DE PRODUCTO
            producto_movimiento_ingreso = detalle_movimiento.filter(Q(estado="ACT") &
                                                                   Q(movimientos__tiendas_destino_id=_id_local) &
                                                                   Q(productos__id=item.id) &
                                                                   Q(movimientos__fue_recibido=True)).aggregate(Sum('cantidad'))['cantidad__sum']
            # ENTRADA DE PRODUCTO
            producto_compra = detalle_compra.filter(Q(estado="ACT") &
                                                         Q(compras__tiendas__id=_id_local) &
                                                         Q(productos__id=item.id)).aggregate(Sum('cantidad'))['cantidad__sum']

            # SALIDA DE PRODUCTO
            entregas_clientes = detalle_entrega.filter(Q(estado="ACT") &
                                                         Q(entregas__tiendas__id=_id_local) &
                                                         Q(productos__id=item.id) &
                                                         Q(entregas__fue_entregado=True)).aggregate(Sum('cantidad'))['cantidad__sum']

            objeto = {
                'nombre_producto': item.nombre,
                'cantidad': (producto_movimiento_ingreso if producto_movimiento_ingreso is not None else 0) - (producto_movimiento_salida if producto_movimiento_salida is not None else 0) + (producto_compra if producto_compra is not None else 0) - (entregas_clientes if entregas_clientes is not None else 0),
                'precio': item.precio_base,
            }
            list.append(objeto)

        serializer = StockProductSerializer(list, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class StockProductByLocalReportListView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = StockProductReportSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        _fecha = self.kwargs['fecha']
        list = []
        for item in Producto.objects.filter(Q(estado="ACT")):
            producto_movimiento_salida = DetalleMovimiento.objects.filter(Q(estado="ACT") &
                                                                          Q(movimientos__tiendas_origen_id=_id_local) &
                                                                          Q(productos__id=item.id) &
                                                                          Q(movimientos__fue_recibido=True) &
                                                                          Q(movimientos__fecha_movimiento__lte=_fecha)).aggregate(Sum('cantidad'))['cantidad__sum']

            producto_movimiento_ingreso = DetalleMovimiento.objects.filter(Q(estado="ACT") &
                                                                           Q(movimientos__tiendas_destino_id=_id_local) &
                                                                           Q(productos__id=item.id) &
                                                                           Q(movimientos__fue_recibido=True) &
                                                                           Q(movimientos__fecha_movimiento__lte=_fecha)).aggregate(Sum('cantidad'))['cantidad__sum']

            producto_compra = DetalleCompra.objects.filter(Q(estado="ACT") &
                                                           Q(compras__tiendas__id=_id_local) &
                                                           Q(productos__id=item.id) &
                                                           Q(compras__fecha_compra__lte=_fecha)).aggregate(Sum('cantidad'))['cantidad__sum']

            entregas_clientes = DetalleEntrega.objects.filter(Q(estado="ACT") &
                                                              Q(entregas__tiendas__id=_id_local) &
                                                              Q(productos__id=item.id) &
                                                              Q(entregas__fue_entregado=True) &
                                                              Q(entregas__fecha_entrega__lte=_fecha)).aggregate(Sum('cantidad'))['cantidad__sum']

            objeto = {
                'id': item.id,
                'nombre_producto': item.nombre,
                'cantidad': (producto_movimiento_ingreso if producto_movimiento_ingreso is not None else 0) - (producto_movimiento_salida if producto_movimiento_salida is not None else 0) + (producto_compra if producto_compra is not None else 0) - (entregas_clientes if entregas_clientes is not None else 0),
            }
            list.append(objeto)

        serializer = StockProductReportSerializer(list, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class MovementWithoutApprovalTransportationAndPreparationDetailView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = MovementWithoutApprovalSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        movimiento = Movimiento.objects.filter(Q(estado="ACT"))

        objeto = {
            'sin_confirmar_recibido': movimiento.filter(Q(fue_recibido=False)).count(),
            'sin_confirmar_trasportado': movimiento.filter(Q(fue_enviado=False)).count(),
            'sin_confirmar_preparado': movimiento.filter(Q(fue_preparado=False)).count(),
        }

        serializer = MovementWithoutApprovalSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleDiscountByLocalAndDailyDataView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = DecimalValueSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id_local = self.kwargs['id']
        current_date = datetime.datetime.now()
        value = DetalleVenta.objects.filter(Q(estado="ACT") &
                                            Q(ventas__tiendas__id=_id_local) &
                                            Q(fecha_venta__day=current_date.day) &
                                            Q(fecha_venta__month=current_date.month) &
                                            Q(fecha_venta__year=current_date.year)).annotate(resultado=F('descuento_unitario')*F('cantidad')).aggregate(Sum('resultado'))['resultado__sum']
        objeto = {
            'valor': value
        }
        serializer = DecimalValueSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)
