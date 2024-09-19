from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from investments.models import InvestmentAccount, Transaction, User, UserAccount
from investments.serializers import InvestmentAccountSerializer, TransactionSerializer, UserAccountSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


