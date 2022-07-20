from rest_framework import serializers
from apps.core.models import *

class TipoMonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMoneda
        fields = '__all__'