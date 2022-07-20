from rest_framework import generics, serializers
from apps.core.models import *
from apps.typesstatesproducts.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class TypeStateProductCreateView(generics.CreateAPIView):
    queryset = TipoEstadoProducto.objects.all()
    serializer_class = TipoEstadoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = TipoEstadoProducto()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class TypeStateProductUpdateView(generics.UpdateAPIView):
    queryset = TipoEstadoProducto.objects.all()
    serializer_class = TipoEstadoProductoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoEstadoProducto.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class TypeStateProductListView(generics.ListAPIView):
    queryset = TipoEstadoProducto.objects.all()
    serializer_class = TipoEstadoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = TipoEstadoProducto.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class TypeStateProductDeleteView(generics.DestroyAPIView):
    queryset = TipoEstadoProducto.objects.all()
    serializer_class = TipoEstadoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoEstadoProducto.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
