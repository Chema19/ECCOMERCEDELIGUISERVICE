from rest_framework import serializers
from apps.core.models import *

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = '__all__'

