# 1️⃣ Imagen base (Python soportado por Koyeb)
FROM python:3.11-slim

# 2️⃣ Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Directorio de trabajo
WORKDIR /app

# 4️⃣ Dependencias del sistema (necesarias para SQLite, psycopg, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Copiar requirements primero (mejor cache)
COPY requirements.txt .

# 6️⃣ Instalar dependencias Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# 7️⃣ Copiar el resto del proyecto
COPY . .

# 8️⃣ Exponer puerto (informativo)
EXPOSE 8000

# 9️⃣ Comando de arranque (PRODUCCIÓN)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:$PORT", "--access-logfile", "-", "--error-logfile", "-"]
