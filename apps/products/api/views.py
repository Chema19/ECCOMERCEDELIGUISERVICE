from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from apps.products.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

class ProductCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Producto()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.precio_base = request.data['precio_base']
        obj.tipoproductos_id = request.data['tipoproductos']
        obj.empresas_id = request.data['empresas']
        obj.tiene_igv = request.data['tiene_igv']
        obj.clientesportales_id = request.data['clientesportales']

        preciobase = request.data['precio_base']
        if float(preciobase) <= float(0):
            return Response({
                'data': None,
                'error': True,
                'message': 'El precio del producto no puede ser menor a cero',
                'code': 400
            })

        obj.descripcion = request.data['descripcion']

        nombre = request.data['nombre']
        validacion_name = Producto.objects.filter(Q(estado='ACT') & Q(nombre=nombre)).exists()
        if validacion_name == True:
            return Response({
                'data': None,
                'error': True,
                'message': 'El nombre del producto ya se encuentra registrado',
                'code': 400
            })

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Producto.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.precio_base = request.data['precio_base']
        obj.tipoproductos_id = request.data['tipoproductos']
        obj.empresas_id = request.data['empresas']
        obj.tiene_igv = request.data['tiene_igv']
        obj.clientesportales_id = request.data['clientesportales']

        preciobase = request.data['precio_base']
        if float(preciobase) <= float(0):
            return Response({
                'data': None,
                'error': True,
                'message': 'El precio del producto no puede ser menor a cero',
                'code': 400
            })

        obj.descripcion = request.data['descripcion']

        nombre = request.data['nombre']
        validacion_name = Producto.objects.filter(Q(estado='ACT') & Q(nombre=nombre) & ~Q(id=_id)).exists()
        if validacion_name == True:
            return Response({
                'data': None,
                'error': True,
                'message': 'El nombre del producto ya se encuentra registrado',
                'code': 400
            })

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class ProductListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'empresas','tiene_igv']

    def list(self, request, *args, **kwargs):
        nombre = request.query_params.get('nombre')
        empresas = request.query_params.get('empresas')
        tiene_igv = request.query_params.get('tiene_igv')

        productos = Producto.objects.filter(Q(estado="ACT")).order_by('-id').all()

        if nombre:
            productos = productos.filter(Q(nombre__icontains=nombre))
        if empresas:
            productos = productos.filter(Q(empresas_id=empresas))
        if tiene_igv == 'Gravado':
            productos = productos.filter(Q(tiene_igv=True))
        elif tiene_igv == 'Exonerado' or tiene_igv == 'Exonerado':
            productos = productos.filter(Q(tiene_igv=False))

        productos_paginated = self.paginate_queryset(productos)
        objs = []
        for item in productos_paginated:
            obj = {
                'id': item.id,
                'nombre': item.nombre,
                'precio_base' : item.precio_base,
                'tipoproductos_id' : item.tipoproductos.id if item.tipoproductos is not None else None,
                'tipoproductos' : item.tipoproductos.nombre if item.tipoproductos is not None else None,
                'empresas_id' : item.empresas.id if item.empresas is not None else None,
                'empresas' : item.empresas.nombre_comercial if item.empresas is not None else None ,
                'tiene_igv' : item.tiene_igv,
                'descripcion' : item.descripcion,
                'estado' : item.estado,
                'fecha_actualizacion' : item.fecha_actualizacion,
                'clientesportales_id': item.clientesportales.id if item.clientesportales is not None else None,
                'clientesportales': item.clientesportales.nombre if item.clientesportales is not None else None
            }
            objs.append(obj)

        serializer = ProductListSerializer(objs, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': productos.count(),
        }
        return Response(result)

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Producto.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Producto.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)