from django.urls import path, include
import investments.views as views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', TokenObtainPairView.as_view(), name="obtain_jwt_token"),
]
