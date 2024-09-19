from django.contrib import admin
from investments.models import User, InvestmentAccount, Transaction, User, UserAccount


# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)
admin.site.register(InvestmentAccount)
admin.site.register(Transaction)
