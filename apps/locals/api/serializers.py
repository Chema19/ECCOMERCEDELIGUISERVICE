from rest_framework import serializers
from apps.core.models import *

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'