from django.db.models import Sum
from .models import InvestmentAccount, Transaction, UserAccount


class InvestmentAccountService:

    @staticmethod
    def get_user_permissions(user, investment_account):
        try:
            return UserAccount.objects.get(user=user, investment_account=investment_account)
        except UserAccount.DoesNotExist:
            return None

    @staticmethod
    def get_user_transactions(user, account_id, start_date=None, end_date=None):
        transactions = Transaction.objects.filter(user=user, investment_account_id=account_id)
        if start_date and end_date:
            transactions = transactions.filter(transaction_date__range=[start_date, end_date])
        total_balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        return transactions, total_balance

    @staticmethod
    def create_transaction(user, account, amount):
        transaction = Transaction.objects.create(user=user, investment_account=account, amount=amount)
        return transaction

    @staticmethod
    def update_account_balance(account):
        total_balance = Transaction.objects.filter(investment_account=account).aggregate(Sum('amount'))['amount__sum'] or 0
        account.balance = total_balance
        account.save()
        return account
