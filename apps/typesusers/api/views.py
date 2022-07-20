from rest_framework import generics, serializers
from apps.core.models import *
from apps.typesusers.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *

class TypeUserCreateView(generics.CreateAPIView):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj = TipoUsuario()
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class TypeUserUpdateView(generics.UpdateAPIView):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoUsuario.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre = request.data['nombre']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class TypeUserListView(generics.ListAPIView):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = TipoUsuario.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class TypeUserDeleteView(generics.DestroyAPIView):
    queryset = TipoUsuario.objects.all()
    serializer_class = TipoUsuarioSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = TipoUsuario.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
