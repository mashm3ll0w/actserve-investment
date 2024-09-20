from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class InvestmentAccount(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(max_length=256, null=False, blank=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.name} - {self.balance}'


class User(AbstractUser):
    username = models.CharField(blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class UserAccount(models.Model):
    VIEW_ONLY = 'view_only'
    FULL_CRUD = 'full_crud'
    POST_ONLY = 'post_only'

    PERMISSION_CHOICES = [
        (VIEW_ONLY, 'View only'),
        (FULL_CRUD, 'Full CRUD'),
        (POST_ONLY, 'Post only')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name="user_account")
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE, null=False, blank=False, related_name='investment_account')
    permissions = models.CharField(max_length=16, choices=PERMISSION_CHOICES, null=False, blank=False)

    class Meta:
        unique_together = ('user', 'investment_account')

    def __str__(self):
        return f'{self.user.username} - {self.investment_account.name}'


class Transaction(models.Model):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer')
    ]

    investment_account = models.ForeignKey(InvestmentAccount, related_name='investment_transactions', on_delete=models.CASCADE, null=False, blank=False)
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=False, related_name="user_transaction")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    transaction_type = models.CharField(max_length=16, choices=TRANSACTION_TYPE_CHOICES, null=False, blank=False)

    def __str__(self):
        return f'{self.investment_account.name} - {self.transaction_type} - {self.amount}'
