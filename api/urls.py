from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para las API ViewSets
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'interactions', views.InteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),  # Para autenticación en browsable API
]
