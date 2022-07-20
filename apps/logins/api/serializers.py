from rest_framework import serializers
from apps.core.models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=500)
    contrasenia = serializers.CharField(max_length=500)


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)
    usuario_id = serializers.IntegerField()
    nombre_completo = serializers.CharField(max_length=500)
    tipousuario_id = serializers.IntegerField()
    nombre_tipousuario = serializers.CharField(max_length=500)
    tienda_id = serializers.IntegerField()
    nombre_tienda = serializers.CharField(max_length=500)
    clienteportal_id = serializers.IntegerField()
    clienteportal = serializers.CharField(max_length=500)