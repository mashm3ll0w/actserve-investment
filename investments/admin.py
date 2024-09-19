from django.contrib import admin
from investments.models import User, InvestmentAccount, Transaction


# Register your models here.
admin.site.register(InvestmentAccount)
admin.site.register(Transaction)
