from rest_framework import serializers
from apps.core.models import *

class PortalCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientePortal
        fields = '__all__'