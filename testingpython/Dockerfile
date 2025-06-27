# --- Etapa 1: Builder ---
# Usamos una imagen base de Python. La versión slim es más ligera.
FROM python:3.12-slim as builder

# Evita que Python genere archivos.pyc y almacene en búfer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalamos `uv`, el gestor de paquetes de Astral
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias
COPY pyproject.toml uv.lock* ./

# Instalamos las dependencias usando uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Copiamos el resto del código de la aplicación
COPY . .

# --- Etapa 2: Final ---
FROM python:3.12-slim

# Configuramos variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalamos dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Instalamos `uv`, el gestor de paquetes de Astral
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Creamos un usuario no-root por seguridad
RUN groupadd --system django && useradd --system --gid django django

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de dependencias
COPY pyproject.toml uv.lock* ./

# Instalamos las dependencias directamente en el sistema Python
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r pyproject.toml

# Copiamos el resto del código de la aplicación
COPY . .

# Cambiamos la propiedad de los archivos al usuario django
RUN chown -R django:django /app

# Cambiamos al usuario no-root
USER django

# Exponemos el puerto
EXPOSE 8000

# Script de entrada para ejecutar migraciones y iniciar el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn testingpython.wsgi:application --bind 0.0.0.0:8000"]
