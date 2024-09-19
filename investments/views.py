from rest_framework import viewsets, filters, permissions, status
from investments.models import InvestmentAccount, Transaction, User, UserAccount
from investments.serializers import InvestmentAccountSerializer, TransactionSerializer, \
    UserAccountSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]




