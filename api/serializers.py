from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User, Company, Customer, Interaction


class CompanySerializer(serializers.ModelSerializer):
    customer_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'customer_count', 'created_at']

    def get_customer_count(self, obj):
        return obj.customers.count()


class UserSerializer(serializers.ModelSerializer):
    customer_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'customer_count', 'is_admin']

    def get_customer_count(self, obj):
        return obj.customers.count()


class InteractionSerializer(serializers.ModelSerializer):
    time_ago = serializers.ReadOnlyField()

    class Meta:
        model = Interaction
        fields = ['id', 'interaction_type', 'notes', 'interaction_date', 'time_ago']


class CustomerListSerializer(serializers.ModelSerializer):
    """Serializer optimizado para la lista de clientes"""
    full_name = serializers.ReadOnlyField()
    birthday_formatted = serializers.ReadOnlyField()
    company_name = serializers.CharField(source='company.name', read_only=True)
    sales_rep_name = serializers.SerializerMethodField()
    last_interaction_info = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'email', 'birthday_formatted',
            'company_name', 'sales_rep_name', 'last_interaction_info',
            'date_of_birth', 'created_at'
        ]

    def get_sales_rep_name(self, obj):
        if obj.sales_rep:
            return f"{obj.sales_rep.first_name} {obj.sales_rep.last_name}".strip() or obj.sales_rep.username
        return None

    def get_last_interaction_info(self, obj):
        last_interaction = obj.last_interaction
        if last_interaction:
            return {
                'type': last_interaction.interaction_type,
                'time_ago': last_interaction.time_ago,
                'date': last_interaction.interaction_date
            }
        return None


class CustomerDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para un cliente específico"""
    full_name = serializers.ReadOnlyField()
    birthday_formatted = serializers.ReadOnlyField()
    company = CompanySerializer(read_only=True)
    sales_rep = UserSerializer(read_only=True)
    interactions = InteractionSerializer(many=True, read_only=True)
    interaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'date_of_birth', 'birthday_formatted', 'company', 'sales_rep',
            'interactions', 'interaction_count', 'created_at', 'updated_at'
        ]

    def get_interaction_count(self, obj):
        return obj.interactions.count()


class CustomerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar clientes"""

    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'date_of_birth',
            'company', 'sales_rep'
        ]

    def validate_email(self, value):
        """Validar que el email sea único"""
        instance = getattr(self, 'instance', None)
        if Customer.objects.exclude(pk=instance.pk if instance else None).filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un cliente con este email.")
        return value


class InteractionCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear interacciones"""

    class Meta:
        model = Interaction
        fields = ['customer', 'interaction_type', 'notes', 'interaction_date']

    def validate_interaction_date(self, value):
        """Validar que la fecha no sea en el futuro"""
        if value > timezone.now():
            raise serializers.ValidationError("La fecha de interacción no puede ser en el futuro.")
        return value
