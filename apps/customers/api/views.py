from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.customers.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

class CustomerCreateView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Cliente()
        obj.estado = 'ACT'
        obj.nombres = request.data['nombres']
        obj.apellidos = request.data['apellidos']
        obj.correo = request.data['correo']
        obj.dni = request.data['dni']
        obj.celular = request.data['celular']
        obj.nombre_completo = request.data['nombre_completo']
        obj.save()

        obj_persona = Persona()
        obj_persona.clientes_id = obj.id
        obj_persona.estado = 'ACT'
        obj_persona.save()

        result = result_success_object(obj,self)
        return Response(result)

class CustomerUpdateView(generics.UpdateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Cliente.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombres = request.data['nombres']
        obj.apellidos = request.data['apellidos']
        obj.correo = request.data['correo']
        obj.dni = request.data['dni']
        obj.celular = request.data['celular']
        obj.nombre_completo = request.data['nombre_completo']
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class CustomerListView(generics.ListAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombres']

    def list(self, request, *args, **kwargs):
        nombres = request.query_params.get('nombres')

        clientes = Cliente.objects.filter(Q(estado="ACT")).order_by('-id').all()
        if nombres:
            clientes = clientes.filter(Q(nombres__icontains=nombres) |
                                       Q(apellidos__icontains=nombres))

        clientes_paginated = self.paginate_queryset(clientes)

        serializer = ClienteSerializer(clientes_paginated, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': clientes.count(),
        }
        return Response(result)

class CustomerDetailView(generics.RetrieveAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Cliente.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class CustomerDeleteView(generics.DestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Cliente.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        Persona.objects.filter(Q(clientes_id=_id)).update(estado="INA")
        result = result_success_object(obj,self)
        return Response(result)
