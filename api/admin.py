from django.contrib import admin
from django.utils.html import format_html
from .models import User, Company, Customer, Interaction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_full_name', 'email', 'is_admin', 'customer_count', 'created_at']
    list_filter = ['is_admin', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = 'Nombre completo'

    def customer_count(self, obj):
        return obj.customers.count()
    customer_count.short_description = 'Clientes asignados'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    def customer_count(self, obj):
        count = obj.customers.count()
        return format_html(
            '<span style="color: #28a745; font-weight: bold;">{}</span>',
            count
        )
    customer_count.short_description = 'Total clientes'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'company', 'sales_rep_name',
        'birthday_formatted', 'interaction_count', 'created_at'
    ]
    list_filter = ['company', 'sales_rep', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'full_name', 'birthday_formatted']
    list_select_related = ['company', 'sales_rep']

    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth')
        }),
        ('Relaciones', {
            'fields': ('company', 'sales_rep')
        }),
        ('Información del Sistema', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def sales_rep_name(self, obj):
        if obj.sales_rep:
            return obj.sales_rep.get_full_name() or obj.sales_rep.username
        return '-'
    sales_rep_name.short_description = 'Representante'

    def interaction_count(self, obj):
        count = obj.interactions.count()
        if count > 0:
            return format_html(
                '<span style="color: #007bff; font-weight: bold;">{}</span>',
                count
            )
        return 0
    interaction_count.short_description = 'Interacciones'


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'interaction_type', 'interaction_date',
        'time_ago', 'notes_preview'
    ]
    list_filter = ['interaction_type', 'interaction_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'notes']
    readonly_fields = ['id', 'time_ago']
    list_select_related = ['customer', 'customer__company']
    date_hierarchy = 'interaction_date'

    fieldsets = (
        ('Información de la Interacción', {
            'fields': ('customer', 'interaction_type', 'interaction_date', 'notes')
        }),
        ('Información del Sistema', {
            'fields': ('id', 'time_ago'),
            'classes': ('collapse',)
        }),
    )

    def notes_preview(self, obj):
        if obj.notes:
            preview = obj.notes[:50]
            if len(obj.notes) > 50:
                preview += '...'
            return preview
        return '-'
    notes_preview.short_description = 'Notas (preview)'
