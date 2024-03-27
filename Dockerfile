FROM python:3.11-alpine

WORKDIR /code

# Copy the .env file from the host to the container's working directory
COPY /etc/secrets/.env .env

ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "acmeportal.wsgi:application", "--bind", "0.0.0.0:8000"]