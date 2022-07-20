from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.locals.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *

class LocalCreateView(generics.CreateAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Tienda()
        obj.estado = 'ACT'
        obj.direccion = request.data['direccion']
        obj.clientesportales_id = request.data['clientesportales']

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class LocalUpdateView(generics.UpdateAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Tienda.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.direccion = request.data['direccion']
        obj.clientesportales_id = request.data['clientesportales']

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class LocalDetailView(generics.RetrieveAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Tienda.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class LocalListView(generics.ListAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        tiendas = Tienda.objects.filter(Q(estado="ACT"))
        if request.query_params['page'] != '':
            locals_paginated = self.paginate_queryset(tiendas)
        else:
            locals_paginated = tiendas

        serializer = TiendaSerializer(locals_paginated, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': tiendas.count(),
        }
        return Response(result)

class LocalDeleteView(generics.DestroyAPIView):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Tienda.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
