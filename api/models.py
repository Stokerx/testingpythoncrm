import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Modelo de usuario personalizado. Hereda de AbstractUser para incluir
    los campos de autenticación de Django y permitir futuras extensiones.
    Representa a un representante de ventas.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username

class Company(models.Model):
    """
    Representa una compañía a la que pertenecen los clientes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class Customer(models.Model):
    """
    Representa a un cliente (persona) asociado a una compañía y
    a un representante de ventas (User).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    # Relaciones
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    sales_rep = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def birthday_formatted(self):
        """Retorna el cumpleaños en formato 'February 5'"""
        return self.date_of_birth.strftime("%B %d")

    @property
    def last_interaction(self):
        """Retorna la última interacción del cliente"""
        return self.interactions.order_by('-interaction_date').first()

    def __str__(self):
        return self.full_name

class Interaction(models.Model):
    """
    Registra una interacción (llamada, email, etc.) entre un
    representante de ventas y un cliente.
    """
    class InteractionType(models.TextChoices):
        CALL = 'Call', 'Call'
        EMAIL = 'Email', 'Email'
        SMS = 'SMS', 'SMS'
        MEETING = 'Meeting', 'Meeting'
        FACEBOOK = 'Facebook', 'Facebook'
        LINKEDIN = 'LinkedIn', 'LinkedIn'
        WHATSAPP = 'WhatsApp', 'WhatsApp'
        PHONE = 'Phone', 'Phone'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=InteractionType.choices)
    notes = models.TextField(blank=True)
    interaction_date = models.DateTimeField()

    class Meta:
        ordering = ['-interaction_date']

    @property
    def time_ago(self):
        """Retorna cuánto tiempo hace que fue la interacción"""
        now = timezone.now()
        diff = now - self.interaction_date

        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

    def __str__(self):
        return f"{self.interaction_type} with {self.customer.full_name} on {self.interaction_date.strftime('%Y-%m-%d')}"