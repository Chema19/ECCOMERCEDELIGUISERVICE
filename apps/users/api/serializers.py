from rest_framework import serializers
from apps.core.models import *

class ColaboradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = '__all__'

class PersonaSelectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=500)
    iduser = serializers.IntegerField()

class UserUpdateStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborador
        fields = ['estado']

class CustomPersonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    empresas_id = serializers.IntegerField()
    empresas_nombre = serializers.CharField(max_length=1000)
    clientes_id = serializers.IntegerField()
    clientes_nombre = serializers.CharField(max_length=1000)
    estado = serializers.CharField(max_length=1000)