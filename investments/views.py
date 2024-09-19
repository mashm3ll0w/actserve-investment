from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from investments.models import InvestmentAccount, Transaction, User
from investments.serializers import InvestmentAccountSerializer, TransactionSerializer, UserSerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_investment_accounts(request):
    queryset = InvestmentAccount.objects.all()
    serializer = InvestmentAccountSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_transactions(request):
    queryset = Transaction.objects.all()
    serializer = TransactionSerializer(queryset, many=True)
    return Response(serializer.data)


