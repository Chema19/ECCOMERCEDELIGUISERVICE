from rest_framework import serializers
from apps.core.models import *

class ProductExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoGasto
        fields = '__all__'
