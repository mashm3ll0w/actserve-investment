from django.urls import path, include
import investments.views as views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'investment_accounts', views.InvestmentAccountViewSet, basename='investment_accounts')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name="obtain_jwt_token"),
]
