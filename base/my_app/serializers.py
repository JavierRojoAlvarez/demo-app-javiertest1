from my_app.models import Cost
from rest_framework import serializers


class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = '__all__'
