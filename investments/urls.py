from django.urls import path, include
import investments.views as views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name="obtain_jwt_token"),
    path('investment_accounts/<int:account_id>/transactions/', views.UserTransactionsView.as_view(), name='user_transactions'),
    path('user_transactions/<int:account_id>', views.AdminView.as_view(), name='admin_user_transactions')
]
