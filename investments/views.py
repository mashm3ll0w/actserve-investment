from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from investments.models import InvestmentAccount, Transaction, User, UserAccount
from investments.permissions import HasAccountPermission, UserViewPermission, AdminViewPermission
from investments.serializers import TransactionSerializer, \
    UserSerializer
from investments.services import InvestmentAccountService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]


class UserTransactionsView(APIView):
    permission_classes = [HasAccountPermission]
    serializer_class = TransactionSerializer(many=True)

    def get(self, request, account_id, format=None):
        investment_account = InvestmentAccount.objects.get(pk=account_id)
        user_account = UserAccount.objects.get(investment_account=investment_account, user=self.request.user)
        account_transactions = Transaction.objects.filter(investment_account=investment_account, user_account=user_account)
        serializer = TransactionSerializer(account_transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminView(APIView):
    permission_classes = [AdminViewPermission]
    serializer_class = TransactionSerializer(many=True)

    def get(self, request, account_id=None):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transactions, total_balance = InvestmentAccountService.get_user_transactions(account_id, start_date, end_date)
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            "transactions": serializer.data,
            "total_balance": total_balance
        })
