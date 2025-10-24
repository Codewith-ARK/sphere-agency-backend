from rest_framework import serializers

from .models import Agency

class AgencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['owner','title', 'type']