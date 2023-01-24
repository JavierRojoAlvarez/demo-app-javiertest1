from cashflows.models import Cashflow
from rest_framework import serializers


class CashflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cashflow
        fields = '__all__'
