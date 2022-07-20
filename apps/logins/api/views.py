from django.contrib.auth.hashers import check_password
from rest_framework import generics, serializers
from apps.core.models import *
from rest_framework.permissions import *
from apps.logins.api.serializers import *
from rest_framework.response import Response
from django.db.models import Q
from apps.core.constants import *

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        contrasenia = request.data['contrasenia']
        try:
            user = Colaborador.objects.get(Q(estado='ACT') & Q(username=username))
        except Colaborador.DoesNotExist:
            json = {
                'data': None,
                'error': True,
                'message': 'Usuario inválido',
                'code': 403
            }
            return Response(json)

        if user.check_password(contrasenia) == False:
            json = {
                'data': None,
                'error': True,
                'message': 'Contraseña inválida',
                'code': 403
            }
            return Response(json)

        objeto = {
            'token':  "token",
            'usuario_id': user.id,
            'nombre_completo': user.nombres + " " + user.apellidos,
            'tipousuario_id': user.tipousuarios_id,
            'nombre_tipousuario': user.tipousuarios.nombre,
            'tienda_id': user.tiendas_id if user.tiendas_id != None else None,
            'nombre_tienda': user.tiendas.direccion if user.tiendas_id != None else None,
            'clienteportal_id': user.clientesportales.id if user.clientesportales_id != None else None,
            'clienteportal': user.clientesportales.nombre if user.clientesportales_id != None else None
        }
        serializer = LoginResponseSerializer(objeto)
        json = {
            'data': serializer.data,
            'error': False,
            'message': 'Success',
            'code': 200
        }
        return Response(json)