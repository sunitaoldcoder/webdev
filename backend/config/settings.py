import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env", override=False)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local-demo-only-change-before-deployment')
DEBUG = os.environ.get('DEBUG', '1') == '1'
if not DEBUG and SECRET_KEY == 'local-demo-only-change-before-deployment':
    raise RuntimeError('Set DJANGO_SECRET_KEY for deployment')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','rest_framework','corsheaders','farmers','farms','advisory','crop_diagnosis','weather','market_prices','experts','feedback','subscriptions','whatsapp','analytics','accounts']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','whitenoise.middleware.WhiteNoiseMiddleware','corsheaders.middleware.CorsMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
if os.environ.get('POSTGRES_HOST'):
    DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql','HOST':os.environ['POSTGRES_HOST'],'NAME':os.environ.get('POSTGRES_DB','agri'),'USER':os.environ.get('POSTGRES_USER','agri'),'PASSWORD':os.environ['POSTGRES_PASSWORD'],'PORT':5432}}
AUTH_PASSWORD_VALIDATORS = [{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator'}]
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.TokenAuthentication','rest_framework.authentication.SessionAuthentication'],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],'DEFAULT_THROTTLE_CLASSES':['rest_framework.throttling.UserRateThrottle','rest_framework.throttling.AnonRateThrottle'],'DEFAULT_THROTTLE_RATES':{'user':'120/hour','anon':'30/hour'},'EXCEPTION_HANDLER':'config.errors.handler'}
INSTALLED_APPS += ['rest_framework.authtoken']
CORS_ALLOWED_ORIGINS = ['http://localhost:5173','http://127.0.0.1:5173']
LANGUAGE_CODE = 'hi'
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
STATIC_URL = 'static/'
MEDIA_ROOT = BASE_DIR/'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATA_UPLOAD_MAX_MEMORY_SIZE = 6 * 1024 * 1024
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True

MIDDLEWARE += ['config.middleware.APILogMiddleware']
LOGGING = {'version':1,'disable_existing_loggers':False,'handlers':{'console':{'class':'logging.StreamHandler'}},'loggers':{'api':{'handlers':['console'],'level':'INFO','propagate':False}}}

# Single-origin HTTPS PWA deployment; source development still uses Vite.
PWA_ROOT = BASE_DIR.parent/'frontend'/'dist'
WHITENOISE_ROOT = PWA_ROOT
WHITENOISE_MAX_AGE = 0  # shell/worker updates must not be hidden by browser caches
STATIC_ROOT = BASE_DIR/'staticfiles'
MEDIA_ROOT = Path(os.environ.get('MEDIA_ROOT', str(BASE_DIR/'media')))
CSRF_TRUSTED_ORIGINS = [x for x in os.environ.get('CSRF_TRUSTED_ORIGINS','').split(',') if x]
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT','0' if DEBUG else '1')=='1'
if os.environ.get('TRUST_PROXY_HEADERS')=='1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
    CSRF_TRUSTED_ORIGINS.append('https://'+os.environ['RENDER_EXTERNAL_HOSTNAME'])
if os.environ.get('DATABASE_URL'):
    from urllib.parse import urlsplit, unquote, parse_qsl
    url=urlsplit(os.environ['DATABASE_URL'])
    if url.scheme not in ('postgres','postgresql'):
        raise RuntimeError('DATABASE_URL must be PostgreSQL')
    DATABASES={'default':{'ENGINE':'django.db.backends.postgresql','NAME':unquote(url.path.lstrip('/')),'USER':unquote(url.username or ''),'PASSWORD':unquote(url.password or ''),'HOST':url.hostname,'PORT':url.port or 5432,'OPTIONS':dict(parse_qsl(url.query))}}
