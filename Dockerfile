# Dockerfile para la aplicación Django
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Exponer puerto de desarrollo
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
