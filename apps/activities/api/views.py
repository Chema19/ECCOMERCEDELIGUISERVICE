from unicodedata import decimal

from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.activities.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *

class ActivityCreateView(generics.CreateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Actividad()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.icono = request.data['icono']
        obj.controlador = request.data['controlador']
        obj.accion = request.data['accion']
        obj.orden = request.data['orden']
        obj.actividad_padre_id = request.data['actividad_padre_id']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class ActivityUpdateView(generics.UpdateAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActivitySerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Actividad.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']
        obj.icono = request.data['icono']
        obj.controlador = request.data['controlador']
        obj.accion = request.data['accion']
        obj.orden = request.data['orden']
        obj.actividad_padre_id = request.data['actividad_padre_id']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class ActivityListView(generics.ListAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        value = Actividad.objects.filter(Q(estado="ACT")).order_by('orden')
        result = result_success_list(value, self)
        return Response(result)

class ActivityDetailView(generics.RetrieveAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Actividad.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class ActivityDeleteView(generics.DestroyAPIView):
    queryset = Actividad.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Actividad.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)