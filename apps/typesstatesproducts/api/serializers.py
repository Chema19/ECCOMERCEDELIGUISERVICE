from rest_framework import serializers
from apps.core.models import *

class TipoEstadoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEstadoProducto
        fields = '__all__'