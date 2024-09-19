from rest_framework import serializers
from investments.models import InvestmentAccount, Transaction, User, UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
