FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=secret,id=proxy_ca,target=/tmp/proxy-ca.pem,required=false \
    if [ -f /tmp/proxy-ca.pem ]; then PIP_CERT=/tmp/proxy-ca.pem pip install --no-cache-dir -r requirements.txt; else pip install --no-cache-dir -r requirements.txt; fi
COPY . .
EXPOSE 8000
CMD ["sh","-c","python manage.py migrate && python manage.py seed_demo && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
