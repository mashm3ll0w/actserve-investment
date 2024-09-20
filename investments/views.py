from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from investments.models import InvestmentAccount, Transaction, User, UserAccount
from investments.permissions import HasAccountPermission, UserViewPermission
from investments.serializers import InvestmentAccountSerializer, TransactionSerializer, \
    UserAccountSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from investments.services import InvestmentAccountService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentAccountSerializer
    queryset = InvestmentAccount.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasAccountPermission]

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


class UserTransactionsView(APIView):
    permission_classes = [HasAccountPermission]
    serializer_class = TransactionSerializer(many=True)

    def get(self, request, account_id, format=None):
        investment_account = InvestmentAccount.objects.get(pk=account_id)
        user_account = UserAccount.objects.get(investment_account=investment_account, user_account=self.request.user)
        account_transactions = Transaction.objects.filter(investment_account=investment_account, user=user_account)
        serializer = TransactionSerializer(account_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
