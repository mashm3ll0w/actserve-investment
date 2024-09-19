from rest_framework import serializers
from investments.models import InvestmentAccount, Transaction


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer)
    class Meta:
        model = Transaction
        fields = '__all__'
