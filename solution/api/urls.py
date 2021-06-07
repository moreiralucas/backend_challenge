from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api.views import (CarViewSet, TyreViewSet)


api_router = routers.DefaultRouter()
api_router.register(r'car', CarViewSet)
api_router.register(r'tyre', TyreViewSet)

urlpatterns = [
    path('', include(api_router.urls), name='api-router'),
]
