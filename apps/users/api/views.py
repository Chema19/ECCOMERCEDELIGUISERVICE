from rest_framework import generics, serializers
from apps.core.models import *
from apps.users.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *
from rest_framework.permissions import *
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class UserCreateView(generics.CreateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        obj = Colaborador()
        obj.estado = 'ACT'
        obj.password = make_password(request.data['password'])
        obj.username = request.data['username']
        obj.apellidos = request.data['apellidos']
        obj.nombres = request.data['nombres']
        obj.email = request.data['email']
        obj.dni = request.data['dni']
        obj.celular = request.data['celular']
        obj.tiendas_id = request.data['tiendas']
        obj.tipousuarios_id = request.data['tipousuarios']
        obj.clientesportales_id = request.data['clientesportales']

        dni = request.data['dni']
        validacion_dni = Colaborador.objects.filter(Q(estado='ACT') & Q(dni=dni)).exists()
        if validacion_dni == True:
            return Response({
                'data': None,
                'error': True,
                'message': 'El dni ya se encuentra registrado',
                'code': 400
            })

        obj.save()
        result = result_success_object(obj,self)
        return Response(result)

class UserUpdateView(generics.UpdateAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Colaborador.objects.get(Q(id=_id))
        obj.estado = 'ACT'
        obj.password = make_password(request.data['password'])
        obj.username = request.data['username']
        obj.apellidos = request.data['apellidos']
        obj.email = request.data['email']
        obj.nombres = request.data['nombres']
        obj.dni = request.data['dni']
        obj.celular = request.data['celular']
        obj.tiendas_id = request.data['tiendas']
        obj.tipousuarios_id = request.data['tipousuarios']
        obj.clientesportales_id = request.data['clientesportales']

        dni = request.data['dni']
        if obj.dni != dni:
            validacion_dni = Colaborador.objects.filter(Q(estado='ACT') & Q(dni=dni)).exists()
            if validacion_dni == True:
                return Response({
                    'data': None,
                    'error': True,
                    'message': 'El dni ya se encuentra registrado',
                    'code': 400
                })

        obj.save()
        result = result_success_object(obj, self)
        return Response(result)

class UserListView(generics.ListAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        value = Colaborador.objects.filter(Q(estado="ACT"))
        result = result_success_list(value, self)
        return Response(result)

class UserDetailView(generics.RetrieveAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        value = Colaborador.objects.get(Q(id=_id))
        result = result_success_object(value, self)
        return Response(result)

class PersonSelectListView(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSelectSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        personas = Persona.objects.filter(Q(estado="ACT"))

        nombre = request.query_params.get('nombre')

        if nombre:
            personas = personas.filter(Q(clientes__nombre_completo__icontains=nombre) |
                                       Q(empresas__nombre_comercial__icontains=nombre))

        personas_paginated = self.paginate_queryset(personas)

        objectos = []
        for item in personas_paginated:
            objeto = {
                'id': item.id,
                'nombre': item.clientes.nombre_completo if item.clientes_id is not None else item.empresas.razon_social,
                'iduser' : item.clientes.id if item.clientes_id is not None else item.empresas.id
            }
            objectos.append(objeto)

        serializer = PersonaSelectSerializer(objectos, many=True)

        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
            'totalelements' : personas.count(),
        }
        return Response(result)

class PersonGetDetailView(generics.ListAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSelectSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        personas = Persona.objects.get(Q(id=_id))
        objeto = {
            'id': personas.id,
            'nombre': personas.clientes.nombre_completo if personas.clientes_id is not None else personas.empresas.razon_social,
            'iduser' : personas.clientes.id if personas.clientes_id is not None else personas.empresas.id
        }

        serializer = PersonaSelectSerializer(objeto)

        result = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200,
        }
        return Response(result)

class UserDeleteView(generics.DestroyAPIView):
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['id']
        obj = Colaborador.objects.get(Q(id=_id))
        obj.estado = "INA"
        obj.save()
        result = result_success_object(obj,self)
        return Response(result)
