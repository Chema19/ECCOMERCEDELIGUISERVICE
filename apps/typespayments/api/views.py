from rest_framework import generics, serializers
from apps.core.models import *
from apps.typespayments.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class TypePaymentCreateView(generics.CreateAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = TipoPago()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class TypePaymentUpdateView(generics.UpdateAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoPago.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class TypePaymentDetailView(generics.RetrieveAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = TipoPago.objects.get(id=_id)
        result = result_success_object(value, self)
        return Response(result)

class TypePaymentListView(generics.ListAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = TipoPago.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class TypePaymentDeleteView(generics.DestroyAPIView):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoPago.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
