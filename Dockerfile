# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN DJANGO_SECRET_KEY=secret python manage.py collectstatic --no-input

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "acmeportal.wsgi:application"]
