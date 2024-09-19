from django.urls import path
import investments.views as views


urlpatterns = [
    path('investment_accounts/', views.get_investment_accounts, name='investment_accounts'),
    path('transactions/', views.get_transactions, name='investment_transactions'),
]
