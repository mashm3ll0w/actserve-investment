from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from investments.models import InvestmentAccount, Transaction, User, UserAccount
from investments.permissions import HasAccountPermission
from investments.serializers import InvestmentAccountSerializer, TransactionSerializer, \
    UserAccountSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

from investments.services import InvestmentAccountService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]


class InvestmentAccountViewSet(APIView):
    serializer_class = InvestmentAccountSerializer
    queryset = InvestmentAccount.objects.all()

    def perform_create(self, serializer):
        account = serializer.save()
        InvestmentAccountService.update_account_balance(account)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [HasAccountPermission]

    def perform_create(self, serializer):
        account = serializer.validated_data.get('investment_account')
        user = self.request.user
        transaction = InvestmentAccountService.create_transaction(user, account, serializer.validated_data['amount'])
        InvestmentAccountService.update_account_balance(account)

    @action(detail=False, methods=['get'], url_path='user-transactions')
    def user_transactions(self, request, account_id=None):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transactions, total_balance = InvestmentAccountService.get_user_transactions(request.user, account_id, start_date, end_date)
        serializer = self.get_serializer(transactions, many=True)
        return Response({
            "transactions": serializer.data,
            "total_balance": total_balance
        })


