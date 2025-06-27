# 🚀 CRM Django + React Application

Una aplicación CRM completa desarrollada con Django REST Framework y React con TypeScript, utilizando PostgreSQL como base de datos y Docker para la containerización.

## 📋 Características

- **Backend Django REST API** con filtros avanzados y paginación
- **Frontend React con TypeScript** y shadcn/ui para una interfaz moderna
- **Base de datos PostgreSQL** para almacenamiento robusto
- **Gestión de datos masivos**: 5 representantes, 2000 clientes, ~213,000 interacciones
- **Filtros inteligentes**: por nombre, cumpleaños, compañía, representante
- **Containerización con Docker** para fácil despliegue
- **Generación automática de datos ficticios** para testing y desarrollo

## 🏗️ Arquitectura

### Backend (Django)
- **Models**: User (representantes), Company, Customer, Interaction
- **API REST** con ViewSets y filtros personalizados
- **Comandos de gestión**: generación de datos ficticios y espera de BD
- **Admin interface** optimizada para CRM
- **Autenticación y permisos** integrados

### Frontend (React + TypeScript)
- **shadcn/ui** para componentes de interfaz
- **Tabla interactiva** con ordenamiento y filtros
- **Estadísticas en tiempo real**
- **Diseño responsive** con Tailwind CSS
- **Comunicación con API** mediante Axios

## 🛠️ Tecnologías

### Backend
- Python 3.12
- Django 5.2.3
- Django REST Framework 3.16.0
- PostgreSQL 16
- Astral UV (gestor de paquetes)
- Faker 37.4.0 (datos ficticios)
- Gunicorn (servidor WSGI)

### Frontend
- React 19 con TypeScript
- shadcn/ui + Radix UI
- Tailwind CSS 3.4.0
- Axios para API calls
- Lucide React (iconos)
- React Table (@tanstack/react-table)

### Infraestructura
- Docker & Docker Compose
- PostgreSQL 16 Alpine
- Node.js 18 Alpine
- Python 3.12 Slim

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Docker y Docker Compose instalados
- Git para clonar el repositorio
- Puerto 3000, 8000 y 5432 disponibles

### Configuración Rápida

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd testingpython
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones si es necesario
   ```

3. **Construir y levantar los servicios**
   ```bash
   # Construir todos los contenedores desde cero
   docker-compose build --no-cache
   
   # Levantar todos los servicios
   docker-compose up -d
   ```

4. **Verificar que los servicios estén funcionando**
   ```bash
   docker-compose ps
   ```

### Generar Datos Ficticios

Para poblar la aplicación con datos de prueba:

```bash
# Generar datos ficticios (5 usuarios, 2000 clientes, 300 interacciones por cliente)
docker exec -it crm_django_web python manage.py generate_fake_data --users 5 --customers 2000 --interactions-per-customer 300

# Verificar que los datos se generaron correctamente
docker exec -it crm_django_web python manage.py shell -c "
from api.models import User, Company, Customer, Interaction
print(f'Usuarios: {User.objects.count()}')
print(f'Empresas: {Company.objects.count()}')
print(f'Clientes: {Customer.objects.count()}')
print(f'Interacciones: {Interaction.objects.count()}')
"
```

## 🌐 Acceso a la Aplicación

Una vez que los contenedores estén ejecutándose:

- **Frontend React**: http://localhost:3000
- **API Django**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin
- **Base de datos PostgreSQL**: localhost:5432

### Credenciales por Defecto

- **Admin Django**: 
  - Usuario: `admin`
  - Contraseña: `admin123`

## 📖 Uso de la API

### Endpoints Principales

#### Clientes
- `GET /api/customers/` - Listar clientes con filtros
- `POST /api/customers/` - Crear nuevo cliente
- `GET /api/customers/{id}/` - Obtener cliente específico
- `PUT/PATCH /api/customers/{id}/` - Actualizar cliente
- `DELETE /api/customers/{id}/` - Eliminar cliente

#### Filtros Disponibles
- `?name=juan` - Buscar por nombre
- `?company=empresa` - Filtrar por empresa
- `?sales_rep=representante` - Filtrar por representante
- `?birthday_this_week=true` - Cumpleaños esta semana
- `?birthday_this_month=true` - Cumpleaños este mes

#### Empresas
- `GET /api/companies/` - Listar empresas
- `GET /api/companies/{id}/customers/` - Clientes de una empresa

#### Usuarios/Representantes
- `GET /api/users/` - Listar representantes
- `GET /api/users/{id}/customers/` - Clientes asignados

#### Interacciones
- `GET /api/interactions/` - Listar interacciones
- `GET /api/interactions/recent/` - Interacciones recientes
- `POST /api/interactions/` - Crear nueva interacción

### Ejemplos de Uso

```bash
# Obtener todos los clientes
curl "http://localhost:8000/api/customers/"

# Buscar clientes por nombre
curl "http://localhost:8000/api/customers/?name=juan"

# Clientes con cumpleaños este mes
curl "http://localhost:8000/api/customers/?birthday_this_month=true"

# Estadísticas de clientes
curl "http://localhost:8000/api/customers/stats/"
```

## 🛠️ Comandos de Desarrollo

### Gestión de Contenedores

```bash
# Ver estado de los servicios
docker-compose ps

# Ver logs de un servicio específico
docker logs crm_django_web
docker logs crm_react_frontend
docker logs crm_postgres_db

# Reiniciar servicios
docker-compose restart

# Detener todos los servicios
docker-compose down

# Reconstruir un servicio específico
docker-compose build web
docker-compose build frontend
```

### Comandos Django

```bash
# Acceder al shell de Django
docker exec -it crm_django_web python manage.py shell

# Crear migraciones
docker exec -it crm_django_web python manage.py makemigrations

# Aplicar migraciones
docker exec -it crm_django_web python manage.py migrate

# Crear superusuario
docker exec -it crm_django_web python manage.py createsuperuser

# Verificar configuración
docker exec -it crm_django_web python manage.py check
```

### Base de Datos

```bash
# Acceder a PostgreSQL
docker exec -it crm_postgres_db psql -U postgres -d crm_db

# Backup de la base de datos
docker exec crm_postgres_db pg_dump -U postgres crm_db > backup.sql

# Restaurar backup
docker exec -i crm_postgres_db psql -U postgres crm_db < backup.sql
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Error: "Connection refused" al ejecutar docker-compose
```bash
# Verificar que Docker esté ejecutándose
systemctl status docker

# Cambiar contexto de Docker si es necesario
docker context use default

# Ajustar permisos del socket
sudo chmod 666 /var/run/docker.sock
```

#### Error: "Cannot filter a query once a slice has been taken"
- Este error ha sido corregido en la versión actual
- Si persiste, verificar que las vistas no apliquen slices antes de filtros

#### Error: "nc: Permission denied"
- Solucionado usando el comando personalizado `wait_for_db.py`
- No es necesario usar `nc` (netcat)

#### Tailwind CSS no funciona
- Asegúrate de que se esté usando Tailwind CSS 3.4.0 (no v4)
- Verificar que existe `postcss.config.js`

### Logs y Debugging

```bash
# Ver logs detallados
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f frontend

# Modo debug para construcción
docker-compose build --no-cache --progress=plain
```

## 📁 Estructura del Proyecto

```
testingpython/
├── docker-compose.yml          # Configuración de contenedores
├── pyproject.toml             # Dependencias Python
├── manage.py                  # Script de gestión Django
├── api/                       # Aplicación Django API
│   ├── models.py             # Modelos de datos
│   ├── views.py              # Vistas API REST
│   ├── serializers.py        # Serializers DRF
│   ├── urls.py               # URLs de la API
│   ├── management/commands/   # Comandos personalizados
│   └── migrations/           # Migraciones de base de datos
├── testingpython/            # Configuración Django
│   ├── settings.py           # Configuración principal
│   ├── urls.py               # URLs principales
│   └── Dockerfile            # Dockerfile para Django
├── frontend/                 # Aplicación React
│   ├── src/                  # Código fuente React
│   ├── public/               # Archivos públicos
│   ├── package.json          # Dependencias Node.js
│   ├── tailwind.config.js    # Configuración Tailwind
│   ├── postcss.config.js     # Configuración PostCSS
│   └── Dockerfile            # Dockerfile para React
└── README.md                 # Documentación
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Django](https://www.djangoproject.com/) - Framework web
- [React](https://reactjs.org/) - Librería de interfaz
- [shadcn/ui](https://ui.shadcn.com/) - Componentes de UI
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS
- [PostgreSQL](https://www.postgresql.org/) - Base de datos
- [Docker](https://www.docker.com/) - Containerización
