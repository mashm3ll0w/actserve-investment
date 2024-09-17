from django.db import models
from django.contrib.auth.models import User


class InvestmentAccount(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(max_length=256, null=False, blank=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


class UserAccount(models.Model):
    VIEW_ONLY = 'view_only'
    FULL_CRUD = 'full_crud'
    POST_ONLY = 'post_only'

    PERMISSION_CHOICES = [
        (VIEW_ONLY, 'View only'),
        (FULL_CRUD, 'Full CRUD'),
        (POST_ONLY, 'Post only')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, null=False, blank=False)
    permissions = models.CharField(max_length=16, choices=PERMISSION_CHOICES, null=False, blank=False)

    class Meta:
        unique_together = ('user', 'investment_account')


class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer')
    ]

    investment_account = models.ForeignKey(InvestmentAccount, related_name='transactions', on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    transaction_type = models.CharField(max_length=16, choices=TRANSACTION_TYPE_CHOICES, null=False, blank=False)
