from unicodedata import decimal

import django_filters
from django.db.models.functions import Upper
from rest_framework import generics, serializers, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from apps.core.models import *
from apps.sales.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q, Sum
from apps.core.constants import *
from decimal import *


class SaleCreateView(generics.CreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = Venta()
        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_venta = request.data['fecha_venta']
        obj.tipopagos_id = request.data['tipopagos']
        obj.tipoestadoproductos_id = request.data['tipoestadoproductos']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']
        obj.tipocomprobante = request.data['tipocomprobante_factura']
        obj.tipoigv = request.data['tipoigv_factura']
        obj.tipopago = request.data['tipopago_factura']
        obj.comprobanteaprobado = request.data['comprobanteaprobado']

        lst_detalles_ventas = request.data['detalles_ventas']
        obj.save()
        for item in lst_detalles_ventas:
            _id_producto = item['productos']
            _precio_original_producto = Producto.objects.get(Q(id=_id_producto)).precio_base

            obj_detalle_venta = DetalleVenta()
            obj_detalle_venta.precio_unitario = item['precio_unitario']
            obj_detalle_venta.precio_sin_descuento = _precio_original_producto
            obj_detalle_venta.cantidad = item['cantidad']
            obj_detalle_venta.total = item['cantidad'] * item['precio_unitario']
            descuento = _precio_original_producto - Decimal(item['precio_unitario'])
            obj_detalle_venta.descuento_unitario = descuento if descuento > 0 else 0
            obj_detalle_venta.productos_id = item['productos']
            obj_detalle_venta.ventas_id = obj.id
            obj_detalle_venta.estado = 'ACT'
            obj_detalle_venta.save()

        lst_sales_credits_boletafactura = request.data['sales_credits_boletafactura']
        for item in lst_sales_credits_boletafactura:
            obj_credito_boletafactrua = CreditoBoletaFactura()
            obj_credito_boletafactrua.fecha_pagar = item['fecha_pagar']
            obj_credito_boletafactrua.monto_pagar = item['monto_pagar']
            obj_credito_boletafactrua.estado = 'ACT'
            obj_credito_boletafactrua.ventas_id = obj.id
            obj_credito_boletafactrua.save()

        if obj.tipocomprobante != 'anulado':
            if obj.tipoigv == 'Gravado':
                obj.total = DetalleVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=obj.id)).aggregate(Sum('total'))[
                    'total__sum']
                _total = obj.total
                obj.impuesto = ((float(_total) * 18.00) / 100.00)
                obj.save()
            else:
                obj.total = DetalleVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=obj.id)).aggregate(Sum('total'))[
                    'total__sum']
                _total = obj.total
                obj.impuesto = float(0.00)
                obj.save()

            #CREDITO VENTA
            creditoVenta = CreditoVenta()
            if request.data['tipopagos'] == 1:#CONTADO
                creditoVenta.fecha_abono =request.data['fecha_venta']
                creditoVenta.monto_pago = _total
                creditoVenta.ventas_id = obj.id
                creditoVenta.estado = 'ACT'
                creditoVenta.personas_id = request.data['personas']
                creditoVenta.descripcion = '-'
                creditoVenta.codigo = request.data['codigo']
                creditoVenta.colaboradores_id = request.data['colaboradores']
                creditoVenta.tiendas_id = request.data['tiendas']
                creditoVenta.tipopagos_id = request.data['tipopagos']
                creditoVenta.tipomonedas_id = request.data['tipomonedas']
                creditoVenta.clientesportales_id = request.data['clientesportales']
                creditoVenta.save()
            elif request.data['tipopagos'] == 6:#TRANSFERENCIA
                creditoVenta.fecha_abono =request.data['fecha_venta']
                creditoVenta.monto_pago = _total
                creditoVenta.ventas_id = obj.id
                creditoVenta.estado = 'ACT'
                creditoVenta.personas_id = request.data['personas']
                creditoVenta.descripcion = '-'
                creditoVenta.codigo = request.data['codigo']
                creditoVenta.colaboradores_id = request.data['colaboradores']
                creditoVenta.tiendas_id = request.data['tiendas']
                creditoVenta.tipopagos_id = request.data['tipopagos']
                creditoVenta.tipomonedas_id = request.data['tipomonedas']
                creditoVenta.clientesportales_id = request.data['clientesportales']
                creditoVenta.save()
            elif request.data['tipopagos'] == 3:#PARTE PAGO
                creditoVenta.fecha_abono = request.data['fecha_venta']
                creditoVenta.monto_pago = request.data['monto_pago']
                creditoVenta.ventas_id = obj.id
                creditoVenta.estado = 'ACT'
                creditoVenta.personas_id = request.data['personas']
                creditoVenta.descripcion = '-'
                creditoVenta.codigo = request.data['codigo']
                creditoVenta.colaboradores_id = request.data['colaboradores']
                creditoVenta.tiendas_id = request.data['tiendas']
                creditoVenta.tipopagos_id = request.data['tipopagos']
                creditoVenta.tipomonedas_id = request.data['tipomonedas']
                creditoVenta.clientesportales_id = request.data['clientesportales']
                creditoVenta.save()

            #ENTREGA
            if request.data['tipoestadoproductos'] == 1:#ENTREGADO
                obj_entrega = Entrega()
                obj_entrega.estado = 'ACT'
                obj_entrega.codigo = request.data['codigo']
                obj_entrega.colaboradores_emisor_id = request.data['colaboradores']
                obj_entrega.colaboradores_transporte_id = request.data['colaboradores']
                obj_entrega.personas_id = request.data['personas']
                obj_entrega.tiendas_id = request.data['tiendas']
                obj_entrega.fue_preparado = True
                obj_entrega.fue_enviado = True
                obj_entrega.fue_entregado = True
                obj_entrega.descripcion = request.data['descripcion']
                obj_entrega.fecha_entrega = request.data['fecha_venta']
                obj_entrega.clientesportales_id = request.data['clientesportales']
                obj_entrega.ventas_id = obj.id
                obj_entrega.save()

                for item in lst_detalles_ventas:
                    obj_detalle_entrega = DetalleEntrega()
                    obj_detalle_entrega.cantidad = item['cantidad']
                    obj_detalle_entrega.productos_id = item['productos']
                    obj_detalle_entrega.entregas_id = obj_entrega.id
                    obj_detalle_entrega.estado = 'ACT'
                    obj_detalle_entrega.save()

            value = Venta.objects.get(Q(id=obj.id))
            detalles_ventas = []
            for item_detalle_venta in DetalleVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado="ACT")):
                detalle_venta = {
                    'id': item_detalle_venta.id,
                    'precio_unitario': item_detalle_venta.precio_unitario,
                    'cantidad': item_detalle_venta.cantidad,
                    'descuento_unitario': item_detalle_venta.descuento_unitario,
                    'precio_sin_descuento': item_detalle_venta.precio_sin_descuento,
                    'productos': item_detalle_venta.productos_id,
                    'ventas': item_detalle_venta.ventas_id,
                    'total': item_detalle_venta.total,
                    'estado': item_detalle_venta.estado
                }
                detalles_ventas.append(detalle_venta)

            creditoventa = CreditoVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
        else:
            obj.total = float(0.00)
            obj.impuesto = float(0.00)
            obj.save()
            detalles_ventas = []
            creditoventa = CreditoVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
            value = Venta.objects.get(Q(id=obj.id))

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'personas': value.personas_id,
            'colaboradores': value.colaboradores_id,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_venta': value.fecha_venta,
            'detalles_ventas': detalles_ventas if len(detalles_ventas) > 0 else None,
            'estado': value.estado,
            'tipopagos': value.tipopagos_id,
            'tipoestadoproductos': value.tipoestadoproductos_id,
            'tipomonedas': value.tipomonedas_id,
            'monto_pago': creditoventa.monto_pago if creditoventa is not None else None,
            'tipocomprobante_factura': value.tipocomprobante,
            'tipoigv_factura': value.tipoigv,
            'tipopago_factura': value.tipopago,
            'clientesportales': value.clientesportales_id,
            'sales_credits_boletafactura': lst_sales_credits_boletafactura if len(lst_sales_credits_boletafactura) > 0 else None,
            'comprobanteaprobado': value.comprobanteaprobado
        }
        serializer = SaleSerializer(objeto)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleUpdateView(generics.UpdateAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Venta.objects.get(Q(id=_id))
        if request.data['tipopagos'] == 3:#PARTE PAGO
            primer_credito_venta = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).order_by('id').first()
            primer_pago = primer_credito_venta.monto_pago if primer_credito_venta is not None else None
            if primer_pago is not None:
                sum_pagos_ventas = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).aggregate(Sum('monto_pago'))['monto_pago__sum']
                if Decimal(sum_pagos_ventas) - Decimal(primer_pago) + Decimal(request.data['monto_pago']) > Decimal(obj.total):
                    result = {
                        'data': None,
                        'error': True,
                        'message': 'Error: El monto de pago y los pagos registrados de la venta superan el total',
                        'code': 400
                    }
                    return Response(result)
                if Decimal(request.data['monto_pago']) > Decimal(obj.total):
                    result = {
                        'data': None,
                        'error': True,
                        'message': 'Error: El monto de pago supera el total de la venta',
                        'code': 400
                    }
                    return Response(result)
        elif request.data['tipopagos'] == 1:#CONTADO
            creditoventahechos = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).count()
            if creditoventahechos > 1:
                result = {
                    'data': None,
                    'error': True,
                    'message': 'Error: No puede cambiar el tipo de pago a contado si ya existen mas de 1 pago registrado para esta venta',
                    'code': 400
                }
                return Response(result)
        elif request.data['tipopagos'] == 6:#TRANSFERENCIA
            creditoventahechos = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).count()
            if creditoventahechos > 1:
                result = {
                    'data': None,
                    'error': True,
                    'message': 'Error: No puede cambiar el tipo de pago a tranferencia si ya existen mas de 1 pago registrado para esta venta',
                    'code': 400
                }
                return Response(result)
        elif request.data['tipopagos'] == 2:#CREDITO
            creditoventahechos = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).count()
            if creditoventahechos > 1:
                result = {
                    'data': None,
                    'error': True,
                    'message': 'Error: No puede cambiar el tipo de pago a credito si ya existen mas de 1 pago registrado para esta venta',
                    'code': 400
                }
                return Response(result)

        obj.estado = 'ACT'
        obj.codigo = request.data['codigo']
        obj.personas_id = request.data['personas']
        obj.colaboradores_id = request.data['colaboradores']
        obj.tiendas_id = request.data['tiendas']
        obj.descripcion = request.data['descripcion']
        obj.fecha_venta = request.data['fecha_venta']
        obj.tipopagos_id = request.data['tipopagos']
        obj.tipoestadoproductos_id = request.data['tipoestadoproductos']
        obj.tipomonedas_id = request.data['tipomonedas']
        obj.clientesportales_id = request.data['clientesportales']
        obj.tipocomprobante = request.data['tipocomprobante_factura']
        obj.tipoigv = request.data['tipoigv_factura']
        obj.tipopago = request.data['tipopago_factura']
        obj.comprobanteaprobado = request.data['comprobanteaprobado']

        lst_detalles_ventas = request.data['detalles_ventas']
        obj.save()

        DetalleVenta.objects.filter(Q(ventas__id=_id)).update(estado='INA')
        for item in lst_detalles_ventas:
            _id_producto = item['productos']
            _precio_original_producto = Producto.objects.get(Q(id=_id_producto)).precio_base
            _id_detalle_venta = item['id']
            if _id_detalle_venta is None:
                obj_detalle_venta = DetalleVenta()
                obj_detalle_venta.precio_unitario = item['precio_unitario']
                obj_detalle_venta.precio_sin_descuento = _precio_original_producto
                obj_detalle_venta.cantidad = item['cantidad']
                obj_detalle_venta.total = item['cantidad'] * item['precio_unitario']
                descuento = _precio_original_producto - Decimal(item['precio_unitario'])
                obj_detalle_venta.descuento_unitario = descuento if descuento > 0 else 0
                obj_detalle_venta.productos_id = item['productos']
                obj_detalle_venta.ventas_id = obj.id
                obj_detalle_venta.estado = 'ACT'
                obj_detalle_venta.save()
                obj.save()
            else:
                obj_detalle_venta = DetalleVenta.objects.get(Q(id=_id_detalle_venta))
                obj_detalle_venta.precio_unitario = item['precio_unitario']
                obj_detalle_venta.precio_sin_descuento = _precio_original_producto
                obj_detalle_venta.cantidad = item['cantidad']
                obj_detalle_venta.total = item['cantidad'] * item['precio_unitario']
                descuento = _precio_original_producto - Decimal(item['precio_unitario'])
                obj_detalle_venta.descuento_unitario = descuento if descuento > 0 else 0
                obj_detalle_venta.productos_id = item['productos']
                obj_detalle_venta.ventas_id = obj.id
                obj_detalle_venta.estado = 'ACT'
                obj_detalle_venta.save()
                obj.save()

        lst_sales_credits_boletafactura = request.data['sales_credits_boletafactura']
        CreditoBoletaFactura.objects.filter(Q(ventas__id=_id)).update(estado='INA')
        for item in lst_sales_credits_boletafactura:
            _id_credito_boletafactrua = item['id']
            if _id_credito_boletafactrua is None:
                obj_credito_boletafactrua = CreditoBoletaFactura()
                obj_credito_boletafactrua.fecha_pagar = item['fecha_pagar']
                obj_credito_boletafactrua.monto_pagar = item['monto_pagar']
                obj_credito_boletafactrua.estado = 'ACT'
                obj_credito_boletafactrua.ventas_id = obj.id
                obj_credito_boletafactrua.save()
            else:
                obj_credito_boletafactrua = CreditoBoletaFactura.objects.get(Q(id=_id_credito_boletafactrua))
                obj_credito_boletafactrua.fecha_pagar = item['fecha_pagar']
                obj_credito_boletafactrua.monto_pagar = item['monto_pagar']
                obj_credito_boletafactrua.estado = 'ACT'
                obj_credito_boletafactrua.ventas_id = obj.id
                obj_credito_boletafactrua.save()

        if obj.tipocomprobante != 'anulado':

            if obj.tipoigv == 'Gravado':
                obj.total = DetalleVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=obj.id)).aggregate(Sum('total'))[
                    'total__sum']
                _total = obj.total
                obj.impuesto = ((float(_total) * 18.00) / 100.00)
                obj.save()
            else:
                obj.total = DetalleVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=obj.id)).aggregate(Sum('total'))[
                    'total__sum']
                _total = obj.total
                obj.impuesto = float(0.00)
                obj.save()

            #CREDITO VENTA
            creditoVenta = CreditoVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
            if request.data['tipopagos'] == 1:#CONTADO
                if creditoVenta is not None:
                    creditoVenta.fecha_abono =request.data['fecha_venta']
                    creditoVenta.monto_pago = _total
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
                else:
                    creditoVenta = CreditoVenta()
                    creditoVenta.fecha_abono = request.data['fecha_venta']
                    creditoVenta.monto_pago = _total
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
            elif request.data['tipopagos'] == 6:  #TRANSFERENCIA
                if creditoVenta is not None:
                    creditoVenta.fecha_abono = request.data['fecha_venta']
                    creditoVenta.monto_pago = _total
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
                else:
                    creditoVenta = CreditoVenta()
                    creditoVenta.fecha_abono = request.data['fecha_venta']
                    creditoVenta.monto_pago = _total
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
            elif request.data['tipopagos'] == 3:#PARTE PAGO
                if creditoVenta is not None:
                    creditoVenta.fecha_abono = request.data['fecha_venta']
                    creditoVenta.monto_pago = request.data['monto_pago']
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
                else:
                    creditoVenta = CreditoVenta()
                    creditoVenta.fecha_abono = request.data['fecha_venta']
                    creditoVenta.monto_pago = request.data['monto_pago']
                    creditoVenta.ventas_id = obj.id
                    creditoVenta.estado = 'ACT'
                    creditoVenta.personas_id = request.data['personas']
                    creditoVenta.descripcion = '-'
                    creditoVenta.codigo = request.data['codigo']
                    creditoVenta.colaboradores_id = request.data['colaboradores']
                    creditoVenta.tiendas_id = request.data['tiendas']
                    creditoVenta.tipopagos_id = request.data['tipopagos']
                    creditoVenta.tipomonedas_id = request.data['tipomonedas']
                    creditoVenta.clientesportales_id = request.data['clientesportales']
                    creditoVenta.save()
            else:  # CREDITO
                CreditoVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=_id)).update(estado="INA")

            #ENTREGA
            entrega = Entrega.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
            if request.data['tipoestadoproductos'] == 1:#ENTREGADO
                if entrega is not None:
                    obj_entrega = Entrega.objects.get(Q(id=entrega.id))
                else:
                    obj_entrega = Entrega()

                obj_entrega.estado = 'ACT'
                obj_entrega.codigo = request.data['codigo']
                obj_entrega.colaboradores_emisor_id = request.data['colaboradores']
                obj_entrega.colaboradores_transporte_id = request.data['colaboradores']
                obj_entrega.tiendas_id = request.data['tiendas']
                obj_entrega.personas_id = request.data['personas']
                obj_entrega.descripcion = request.data['descripcion']
                obj_entrega.fecha_entrega = request.data['fecha_venta']
                obj_entrega.fue_preparado = True
                obj_entrega.fue_enviado = True
                obj_entrega.fue_entregado = True
                obj_entrega.ventas_id = obj.id
                obj_entrega.clientesportales_id = request.data['clientesportales']
                obj_entrega.save()

                if entrega is not None:
                    DetalleEntrega.objects.filter(Q(entregas__id=entrega.id)).update(estado='INA')

                for item in lst_detalles_ventas:
                    obj_detalle_entrega = DetalleEntrega()
                    obj_detalle_entrega.cantidad = item['cantidad']
                    obj_detalle_entrega.productos_id = item['productos']
                    obj_detalle_entrega.entregas_id = obj_entrega.id
                    obj_detalle_entrega.estado = 'ACT'
                    obj_detalle_entrega.save()
            else:
                if entrega is not None:
                    Entrega.objects.filter(Q(estado="ACT") & Q(ventas__id=_id) & Q(id=entrega.id)).update(estado="INA")
                    DetalleEntrega.objects.filter(Q(estado="ACT") & Q(entregas__id=entrega.id)).update(estado="INA")
            value = Venta.objects.get(Q(id=obj.id))

            detalles_ventas = []
            for item_detalle_venta in DetalleVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado="ACT")):
                detalle_venta = {
                    'id': item_detalle_venta.id,
                    'precio_unitario': item_detalle_venta.precio_unitario,
                    'cantidad': item_detalle_venta.cantidad,
                    'descuento_unitario': item_detalle_venta.descuento_unitario,
                    'precio_sin_descuento': item_detalle_venta.precio_sin_descuento,
                    'productos': item_detalle_venta.productos_id,
                    'ventas': item_detalle_venta.ventas_id,
                    'total': item_detalle_venta.total,
                    'estado': item_detalle_venta.estado
                }
                detalles_ventas.append(detalle_venta)

            creditos_ventas_boletafactura = []
            for item_credito_venta_boletafactura in CreditoBoletaFactura.objects.filter(Q(ventas__id=obj.id) & Q(estado="ACT")):
                credito_venta_boletafactura = {
                    'id': item_credito_venta_boletafactura.id,
                    'fecha_pagar': item_credito_venta_boletafactura.fecha_pagar,
                    'monto_pagar': item_credito_venta_boletafactura.monto_pagar,
                    'ventas': item_credito_venta_boletafactura.ventas_id,
                    'estado': item_credito_venta_boletafactura.estado
                }
                creditos_ventas_boletafactura.append(credito_venta_boletafactura)

            creditoventa = CreditoVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
        else:

            obj.total = float(0.00)
            obj.impuesto = float(0.00)
            obj.save()
            detalles_ventas = []
            creditos_ventas_boletafactura = []
            creditoventa = CreditoVenta.objects.filter(Q(ventas__id=obj.id) & Q(estado='ACT')).order_by('id').first()
            value = Venta.objects.get(Q(id=obj.id))

        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'personas': value.personas_id,
            'colaboradores': value.colaboradores_id,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_venta': value.fecha_venta,
            'detalles_ventas': detalles_ventas if len(detalles_ventas) > 0 else None,
            'sales_credits_boletafactura': creditos_ventas_boletafactura if len(creditos_ventas_boletafactura) > 0 else None,
            'estado': value.estado,
            'tipopagos': value.tipopagos_id,
            'tipoestadoproductos': value.tipoestadoproductos_id,
            'tipomonedas': value.tipomonedas_id,
            'monto_pago': creditoventa.monto_pago if creditoventa is not None else None,
            'tipocomprobante_factura': value.tipocomprobante,
            'tipoigv_factura': value.tipoigv,
            'tipopago_factura': value.tipopago,
            'clientesportales': value.clientesportales_id,
            'comprobanteaprobado': value.comprobanteaprobado
        }
        serializer = SaleSerializer(objeto)

        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleUpdateVoucherFieldView(generics.UpdateAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleApprovalVoucherSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Venta.objects.get(Q(id=_id))

        obj.estado = 'ACT'
        obj.comprobanteaprobado = request.data['comprobanteaprobado']
        obj.save()

        objeto = {
            'id': obj.id,
            'comprobanteaprobado': obj.comprobanteaprobado,
        }
        serializer = SaleApprovalVoucherSerializer(objeto)

        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleListView(generics.ListAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['codigo', 'fecha_venta', 'tiendas__id', 'personas']

    def list(self, request, *args, **kwargs):
        #_tiendaid = self.kwargs['tiendaid']
        personas = request.query_params.get('personas')
        tiendas = request.query_params.get('tiendas__id')
        fecha_venta = request.query_params.get('fecha_venta')
        codigo = request.query_params.get('codigo')

        ventas = Venta.objects.filter(estado="ACT").order_by('-id').all()

        if personas:
            ventas = ventas.filter(Q(personas__clientes__nombres__icontains=personas) | Q(personas__clientes__apellidos__icontains=personas) | Q(personas__empresas__nombre_comercial__icontains=personas))
        if tiendas:
            ventas = ventas.filter(tiendas_id= tiendas)
        if fecha_venta:
            ventas = ventas.filter(fecha_venta=fecha_venta)
        if codigo:
            ventas = ventas.filter(codigo=codigo)

        ventas_paginated = self.paginate_queryset(ventas)
        objectos = []
        for item in ventas_paginated:
            objeto = {
                'id': item.id,
                'codigo': item.codigo,
                'tiendas': item.tiendas.direccion,
                'tiendas_id': item.tiendas.id,
                'personas': item.personas.clientes.nombres + " " + item.personas.clientes.apellidos if item.personas.clientes_id is not None else item.personas.empresas.nombre_comercial,
                'personas_id': item.personas.id,
                'fecha_venta': item.fecha_venta,
                'estado': item.estado,
                'tipo_pago': item.tipopagos.nombre,
                'tipo_estado_producto': item.tipoestadoproductos.nombre,
                'tipo_moneda': item.tipomonedas.nombre,
                'tipocomprobante_factura': item.tipocomprobante,
                'tipoigv_factura': item.tipoigv,
                'tipopago_factura': item.tipopago,
                'clientesportales': item.clientesportales.nombre,
                'clientesportales_id': item.clientesportales_id,
                'comprobanteaprobado': item.comprobanteaprobado,
            }
            objectos.append(objeto)
        serializer = SaleListSerializer(objectos, many=True)
        result = {
           'data': serializer.data,
           'error': False,
           'message': 'Success',
           'code': 200,
            'totalelements': ventas.count(),
        }
        return Response(result)

class SaleDetailView(generics.RetrieveAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Venta.objects.get(Q(id=_id))

        detalles_ventas = []
        for item_detalle_venta in DetalleVenta.objects.filter(ventas__id=_id,estado="ACT"):
            detalle_venta = {
                'id': item_detalle_venta.id,
                'precio_unitario': item_detalle_venta.precio_unitario,
                'cantidad': item_detalle_venta.cantidad,
                'descuento_unitario' : item_detalle_venta.descuento_unitario,
                'precio_sin_descuento': item_detalle_venta.precio_sin_descuento,
                'productos': item_detalle_venta.productos_id,
                'ventas': item_detalle_venta.ventas_id,
                'total': item_detalle_venta.total,
                'estado': item_detalle_venta.estado
            }
            detalles_ventas.append(detalle_venta)

        creditos_ventas_boletafactura = []
        for item_credito_ventas_boletafactura in CreditoBoletaFactura.objects.filter(ventas__id=_id, estado="ACT"):
            credito_venta_boletafactura = {
                'id': item_credito_ventas_boletafactura.id,
                'fecha_pagar': item_credito_ventas_boletafactura.fecha_pagar,
                'monto_pagar': item_credito_ventas_boletafactura.monto_pagar,
                'estado': item_credito_ventas_boletafactura.estado,
                'ventas': item_credito_ventas_boletafactura.ventas_id
            }
            creditos_ventas_boletafactura.append(credito_venta_boletafactura)

        creditoventa = CreditoVenta.objects.filter(Q(ventas__id=_id) & Q(estado='ACT')).order_by('id').first()
        objeto = {
            'id': value.id,
            'codigo': value.codigo,
            'personas': value.personas_id,
            'colaboradores': value.colaboradores_id,
            'tiendas': value.tiendas_id,
            'descripcion': value.descripcion,
            'fecha_venta': value.fecha_venta,
            'detalles_ventas': detalles_ventas,
            'sales_credits_boletafactura': creditos_ventas_boletafactura,
            'estado': value.estado,
            'tipopagos': value.tipopagos_id,
            'tipoestadoproductos': value.tipoestadoproductos_id,
            'tipomonedas': value.tipomonedas_id,
            'monto_pago': creditoventa.monto_pago if creditoventa is not None else None,
            'tipocomprobante_factura': value.tipocomprobante,
            'tipoigv_factura': value.tipoigv,
            'tipopago_factura': value.tipopago,
            'clientesportales': value.clientesportales_id,
            'comprobanteaprobado': value.comprobanteaprobado,
        }

        serializer = SaleSerializer(objeto, many=False)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)

class SaleDeleteView(generics.DestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = SaleSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Venta.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        DetalleVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=_id)).update(estado="INA")

        creditoventa = CreditoVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=_id))
        if creditoventa is not None:
            CreditoVenta.objects.filter(Q(estado="ACT") & Q(ventas__id=_id)).update(estado="INA")

        entrega = Entrega.objects.filter(Q(estado="ACT") & Q(ventas__id=_id))
        if entrega is not None:
            Entrega.objects.filter(Q(estado="ACT") & Q(ventas__id=_id)).update(estado="INA")
            DetalleEntrega.objects.filter(Q(estado="ACT") & Q(entregas__ventas__id=_id)).update(estado="INA")
        result = {
            'data': None,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(result)