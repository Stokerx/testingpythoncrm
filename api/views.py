from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Prefetch
from django.utils import timezone
from datetime import datetime, timedelta
import django_filters

from .models import User, Company, Customer, Interaction
from .serializers import (
    UserSerializer, CompanySerializer, CustomerListSerializer,
    CustomerDetailSerializer, CustomerCreateUpdateSerializer,
    InteractionSerializer, InteractionCreateSerializer
)


class CustomerFilter(django_filters.FilterSet):
    """Filtros personalizados para clientes"""
    name = django_filters.CharFilter(method='filter_by_name')
    birthday_this_week = django_filters.BooleanFilter(method='filter_birthday_this_week')
    birthday_this_month = django_filters.BooleanFilter(method='filter_birthday_this_month')
    company = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    sales_rep = django_filters.CharFilter(method='filter_by_sales_rep')

    class Meta:
        model = Customer
        fields = ['company', 'sales_rep']

    def filter_by_name(self, queryset, name, value):
        """Filtrar por nombre completo"""
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )

    def filter_birthday_this_week(self, queryset, name, value):
        """Filtrar clientes con cumpleaños esta semana"""
        if not value:
            return queryset

        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        return queryset.filter(
            date_of_birth__month__in=[start_of_week.month, end_of_week.month],
            date_of_birth__day__range=[start_of_week.day, end_of_week.day]
        )

    def filter_birthday_this_month(self, queryset, name, value):
        """Filtrar clientes con cumpleaños este mes"""
        if not value:
            return queryset

        current_month = timezone.now().month
        return queryset.filter(date_of_birth__month=current_month)

    def filter_by_sales_rep(self, queryset, name, value):
        """Filtrar por nombre del representante de ventas"""
        return queryset.filter(
            Q(sales_rep__first_name__icontains=value) |
            Q(sales_rep__last_name__icontains=value) |
            Q(sales_rep__username__icontains=value)
        )


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clientes con funcionalidades de CRM"""
    queryset = Customer.objects.select_related('company', 'sales_rep').prefetch_related('interactions')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    ordering_fields = ['first_name', 'last_name', 'company__name', 'date_of_birth', 'created_at']
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'list':
            return CustomerListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomerCreateUpdateSerializer
        return CustomerDetailSerializer

    def get_queryset(self):
        """Obtener queryset optimizado según la acción"""
        queryset = Customer.objects.select_related('company', 'sales_rep')

        if self.action == 'list':
            # Para la lista, solo prefetch las interacciones más recientes
            queryset = queryset.prefetch_related(
                Prefetch(
                    'interactions',
                    queryset=Interaction.objects.order_by('-interaction_date'),
                    to_attr='recent_interactions'
                )
            )
        else:
            # Para detalle, incluir todas las interacciones
            queryset = queryset.prefetch_related('interactions')

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas generales de clientes"""
        base_queryset = Customer.objects.all()
        total_customers = base_queryset.count()
        birthday_this_week = CustomerFilter().filter_birthday_this_week(
            base_queryset, None, True
        ).count()
        birthday_this_month = CustomerFilter().filter_birthday_this_month(
            base_queryset, None, True
        ).count()

        return Response({
            'total_customers': total_customers,
            'birthday_this_week': birthday_this_week,
            'birthday_this_month': birthday_this_month,
        })

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """Obtener todas las interacciones de un cliente"""
        customer = self.get_object()
        interactions = customer.interactions.all()
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar compañías"""
    queryset = Company.objects.prefetch_related('customers')
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Obtener todos los clientes de una compañía"""
        company = self.get_object()
        customers = company.customers.select_related('sales_rep').prefetch_related('interactions')
        serializer = CustomerListSerializer(customers, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios/representantes de ventas"""
    queryset = User.objects.prefetch_related('customers')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'created_at']
    ordering = ['first_name', 'last_name']

    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Obtener todos los clientes asignados a un representante"""
        user = self.get_object()
        customers = user.customers.select_related('company').prefetch_related('interactions')
        serializer = CustomerListSerializer(customers, many=True)
        return Response(serializer.data)


class InteractionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar interacciones"""
    queryset = Interaction.objects.select_related('customer', 'customer__company')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['interaction_type', 'customer']
    search_fields = ['notes', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['interaction_date', 'interaction_type']
    ordering = ['-interaction_date']

    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return InteractionCreateSerializer
        return InteractionSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtener interacciones recientes (últimos 7 días)"""
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_interactions = self.get_queryset().filter(
            interaction_date__gte=seven_days_ago
        )
        serializer = self.get_serializer(recent_interactions, many=True)
        return Response(serializer.data)
