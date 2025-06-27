from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from faker import Faker
import random
from datetime import datetime, timedelta

from api.models import User, Company, Customer, Interaction

fake = Faker(['es_ES', 'en_US'])  # Usar datos en español e inglés


class Command(BaseCommand):
    help = 'Genera datos ficticios para el CRM: 3 representantes, 1000 clientes y ~500,000 interacciones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Número de representantes de ventas a crear (default: 3)'
        )
        parser.add_argument(
            '--customers',
            type=int,
            default=1000,
            help='Número de clientes a crear (default: 1000)'
        )
        parser.add_argument(
            '--interactions-per-customer',
            type=int,
            default=500,
            help='Número de interacciones por cliente (default: 500)'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Iniciando generación de datos ficticios...')
        )

        # Limpiar datos existentes
        self.stdout.write('🧹 Limpiando datos existentes...')
        Interaction.objects.all().delete()
        Customer.objects.all().delete()
        Company.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Crear representantes de ventas
        self.stdout.write('👥 Creando representantes de ventas...')
        users = self.create_sales_reps(options['users'])

        # Crear compañías
        self.stdout.write('🏢 Creando compañías...')
        companies = self.create_companies()

        # Crear clientes
        self.stdout.write('👤 Creando clientes...')
        customers = self.create_customers(
            options['customers'],
            companies,
            users
        )

        # Crear interacciones
        self.stdout.write('📞 Creando interacciones...')
        self.create_interactions(
            customers,
            options['interactions_per_customer']
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ ¡Datos generados exitosamente!\n'
                f'   📊 {len(users)} representantes de ventas\n'
                f'   🏢 {len(companies)} compañías\n'
                f'   👥 {len(customers)} clientes\n'
                f'   📞 ~{len(customers) * options["interactions_per_customer"]:,} interacciones'
            )
        )

    def create_sales_reps(self, count):
        """Crear representantes de ventas"""
        users = []
        for i in range(count):
            user = User.objects.create_user(
                username=f'rep_{i+1}',
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_admin=i == 0  # El primer usuario será admin
            )
            users.append(user)
            self.stdout.write(f'   ✓ {user.get_full_name()} ({user.username})')

        return users

    def create_companies(self):
        """Crear compañías diversas"""
        company_names = [
            'TechCorp Solutions', 'Global Industries', 'Innovation Labs',
            'Digital Dynamics', 'Future Systems', 'Elite Enterprises',
            'Prime Technology', 'Advanced Solutions', 'Smart Industries',
            'NextGen Corp', 'Alpha Technologies', 'Beta Systems',
            'Gamma Solutions', 'Delta Industries', 'Omega Tech',
            'Synergy Group', 'Quantum Labs', 'Vertex Solutions',
            'Matrix Corp', 'Phoenix Systems', 'Stellar Technologies',
            'Apex Industries', 'Zenith Solutions', 'Summit Corp',
            'Pinnacle Tech', 'Horizon Systems', 'Catalyst Group',
            'Nexus Solutions', 'Prism Technologies', 'Eclipse Corp'
        ]

        companies = []
        for name in company_names:
            company = Company.objects.create(name=name)
            companies.append(company)

        self.stdout.write(f'   ✓ {len(companies)} compañías creadas')
        return companies

    def create_customers(self, count, companies, users):
        """Crear clientes con datos realistas"""
        customers = []

        for i in range(count):
            # Generar fecha de nacimiento realista (entre 18 y 80 años)
            min_age = 18
            max_age = 80
            birth_date = fake.date_of_birth(
                minimum_age=min_age,
                maximum_age=max_age
            )

            customer = Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.unique.email(),
                date_of_birth=birth_date,
                company=random.choice(companies),
                sales_rep=random.choice(users)
            )
            customers.append(customer)

            # Mostrar progreso cada 100 clientes
            if (i + 1) % 100 == 0:
                self.stdout.write(f'   ✓ {i + 1} clientes creados...')

        self.stdout.write(f'   ✅ {count} clientes creados en total')
        return customers

    def create_interactions(self, customers, interactions_per_customer):
        """Crear interacciones masivas de forma eficiente"""
        interaction_types = [
            'Call', 'Email', 'SMS', 'Meeting',
            'Facebook', 'LinkedIn', 'WhatsApp', 'Phone'
        ]

        # Notas de ejemplo para las interacciones
        sample_notes = [
            'Cliente interesado en el producto',
            'Seguimiento de propuesta comercial',
            'Reunión de presentación programada',
            'Cliente solicita más información',
            'Negociación de precios',
            'Firma de contrato pendiente',
            'Soporte técnico requerido',
            'Renovación de contrato',
            'Cliente satisfecho con el servicio',
            'Feedback positivo recibido',
            'Problema técnico resuelto',
            'Nueva oportunidad de negocio',
            'Referencia a otros clientes',
            'Actualización de datos',
            'Confirmación de entrega',
            ''  # Nota vacía ocasional
        ]

        interactions_to_create = []
        total_interactions = 0

        for customer in customers:
            # Generar interacciones para este cliente
            for j in range(interactions_per_customer):
                # Fecha aleatoria en los últimos 2 años
                max_days_ago = 730  # 2 años
                days_ago = random.randint(0, max_days_ago)
                interaction_date = timezone.now() - timedelta(days=days_ago)

                # Agregar algo de variación en horas
                interaction_date += timedelta(
                    hours=random.randint(8, 18),  # Horario laboral
                    minutes=random.randint(0, 59)
                )

                interaction = Interaction(
                    customer=customer,
                    interaction_type=random.choice(interaction_types),
                    notes=random.choice(sample_notes),
                    interaction_date=interaction_date
                )
                interactions_to_create.append(interaction)
                total_interactions += 1

                # Crear en lotes de 1000 para eficiencia
                if len(interactions_to_create) >= 1000:
                    Interaction.objects.bulk_create(interactions_to_create)
                    interactions_to_create = []
                    self.stdout.write(f'   ✓ {total_interactions:,} interacciones creadas...')

        # Crear las interacciones restantes
        if interactions_to_create:
            Interaction.objects.bulk_create(interactions_to_create)

        self.stdout.write(f'   ✅ {total_interactions:,} interacciones creadas en total')
