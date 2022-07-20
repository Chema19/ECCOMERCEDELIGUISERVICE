from rest_framework import generics, serializers
from apps.core.models import *
from apps.portalscustomers.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class PortalCustomerCreateView(generics.CreateAPIView):
    queryset = ClientePortal.objects.all()
    serializer_class = PortalCustomerSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = ClientePortal()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class PortalCustomerUpdateView(generics.UpdateAPIView):
    queryset = ClientePortal.objects.all()
    serializer_class = PortalCustomerSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = ClientePortal.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class PortalCustomerListView(generics.ListAPIView):
    queryset = ClientePortal.objects.all()
    serializer_class = PortalCustomerSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = ClientePortal.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class PortalCustomerDeleteView(generics.DestroyAPIView):
    queryset = ClientePortal.objects.all()
    serializer_class = PortalCustomerSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = ClientePortal.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
