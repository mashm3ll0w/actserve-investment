from django.urls import path, include
import investments.views as views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
