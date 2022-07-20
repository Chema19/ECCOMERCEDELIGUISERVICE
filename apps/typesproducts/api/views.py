from rest_framework import generics, serializers
from apps.core.models import *
from apps.typesproducts.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class TypeProductCreateView(generics.CreateAPIView):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = TipoProducto()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class TypeProductUpdateView(generics.UpdateAPIView):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoProducto.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class TypeProductListView(generics.ListAPIView):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = TipoProducto.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class TypeProductDeleteView(generics.DestroyAPIView):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoProducto.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
