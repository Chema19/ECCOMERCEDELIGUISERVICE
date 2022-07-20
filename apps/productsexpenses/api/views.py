from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.productsexpenses.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *

class ProductExpensesCreateView(generics.CreateAPIView):
    queryset = ProductoGasto.objects.all()
    serializer_class = ProductExpensesSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = ProductoGasto()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        nombre = request.data['nombre']
        validacion_name = ProductoGasto.objects.filter(Q(estado='ACT') & Q(nombre=nombre)).exists()
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

class ProductExpensesUpdateView(generics.UpdateAPIView):
    queryset = ProductoGasto.objects.all()
    serializer_class = ProductExpensesSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = ProductoGasto.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        nombre = request.data['nombre']
        validacion_name = ProductoGasto.objects.filter(Q(estado='ACT') & Q(nombre=nombre) & ~Q(id=_id)).exists()
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

class ProductExpensesListView(generics.ListAPIView):
    queryset = ProductoGasto.objects.all()
    serializer_class = ProductExpensesSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        value = ProductoGasto.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class ProductExpensesDetailView(generics.RetrieveAPIView):
    queryset = ProductoGasto.objects.all()
    serializer_class = ProductExpensesSerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = ProductoGasto.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class ProductExpensesDeleteView(generics.DestroyAPIView):
    queryset = ProductoGasto.objects.all()
    serializer_class = ProductExpensesSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = ProductoGasto.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)