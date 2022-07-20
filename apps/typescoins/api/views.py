from rest_framework import generics, serializers
from apps.core.models import *
from apps.typescoins.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class TypeCoinCreateView(generics.CreateAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = TipoMoneda()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.abreviacion = request.data['abreviacion']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class TypeCoinUpdateView(generics.UpdateAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoMoneda.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.abreviacion = request.data['abreviacion']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class TypeCoinDetailView(generics.RetrieveAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoMonedaSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = TipoMoneda.objects.get(id=_id)
        result = result_success_object(value, self)
        return Response(result)

class TypeCoinListView(generics.ListAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = TipoMoneda.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class TypeCoinDeleteView(generics.DestroyAPIView):
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoMoneda.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
