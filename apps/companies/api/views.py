from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from apps.core.models import *
from apps.companies.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

class CompanyCreateView(generics.CreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        obj = Empresa()
        obj.estado = 'ACT'
        obj.nombre_comercial = request.data['nombre_comercial']
        obj.razon_social = request.data['razon_social']
        obj.correo = request.data['correo']
        obj.RUC = request.data['RUC']
        obj.celular = request.data['celular']
        obj.save()

        obj_persona = Persona()
        obj_persona.empresas_id = obj.id
        obj_persona.estado = 'ACT'
        obj_persona.save()

        result = result_success_object(obj,self)
        return Response(result)

class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    lookup_field = "id"
    permission_classes = (IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Empresa.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.nombre_comercial = request.data['nombre_comercial']
        obj.razon_social = request.data['razon_social']
        obj.correo = request.data['correo']
        obj.RUC = request.data['RUC']
        obj.celular = request.data['celular']
        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class CompanyListView(generics.ListAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre_comercial']

    def list(self, request, *args, **kwargs):
        nombre_comercial = request.query_params.get('nombre_comercial')

        empresas = Empresa.objects.filter(Q(estado="ACT")).order_by('-id').all()

        if nombre_comercial:
            empresas = empresas.filter(Q(nombre_comercial__icontains=nombre_comercial) |
                                     Q(razon_social__icontains=nombre_comercial))

        empresas_paginated = self.paginate_queryset(empresas)


        serializer = EmpresaSerializer(empresas_paginated, many=True)
        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements': empresas.count(),
        }
        return Response(result)

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Empresa.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class CompanyDeleteView(generics.DestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Empresa.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        Persona.objects.filter(Q(empresas_id=_id)).update(estado="INA")
        result = result_success_object(obj,self)
        return Response(result)
