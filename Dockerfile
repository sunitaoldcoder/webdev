# One web service: React PWA assets + Django API on the same HTTPS origin.
FROM node:24-alpine AS ui
WORKDIR /ui
COPY frontend/package*.json ./
RUN --mount=type=secret,id=proxy_ca,target=/tmp/proxy-ca.pem,required=false \
    if [ -f /tmp/proxy-ca.pem ]; then NODE_EXTRA_CA_CERTS=/tmp/proxy-ca.pem npm ci; else npm ci; fi
COPY frontend/ .
RUN npm run build
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN --mount=type=secret,id=proxy_ca,target=/tmp/proxy-ca.pem,required=false \
    if [ -f /tmp/proxy-ca.pem ]; then PIP_CERT=/tmp/proxy-ca.pem pip install --no-cache-dir -r requirements.txt; else pip install --no-cache-dir -r requirements.txt; fi
COPY backend/ .
COPY --from=ui /ui/dist /app/frontend/dist
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["sh","-c","python manage.py migrate && python manage.py seed_crops && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --access-logfile -"]
