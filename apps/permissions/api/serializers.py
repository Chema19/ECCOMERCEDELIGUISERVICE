from rest_framework import serializers
from apps.core.models import *

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'


class PermisionActivitySonSerializer(serializers.Serializer):
    actividades = serializers.IntegerField()
    actividades_nombre = serializers.CharField(max_length=500)
    controlador = serializers.CharField(max_length=500)
    accion = serializers.CharField(max_length=500)
    tiposussuarios = serializers.IntegerField()
    tiposussuarios_nombre = serializers.CharField(max_length=500)
    visualizar = serializers.BooleanField()
    editar = serializers.BooleanField()
    importar = serializers.BooleanField()
    exportar = serializers.BooleanField()
    estado = serializers.CharField(max_length=10)

class PermisionActivityFatherSerializer(serializers.Serializer):
    actividades = serializers.IntegerField()
    actividades_nombre = serializers.CharField(max_length=500)
    icono = serializers.CharField(max_length=500)
    visualizar = serializers.BooleanField()
    tiposussuarios = serializers.IntegerField()
    tiposussuarios_nombre = serializers.CharField(max_length=500)
    detalles_permissions_activities_sons = PermisionActivitySonSerializer(many=True)
    estado = serializers.CharField(max_length=10)