from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'tu-secreta-key-para-django'

DEBUG = False  # Cambia a False en producción

# Actualizado con el nombre de tu dominio en Render
ALLOWED_HOSTS = ['chatenlinea-8omv.onrender.com', 'localhost', '127.0.0.1']

# Agregar el dominio a CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = ['https://chatenlinea-8omv.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',  # O el nombre de tu aplicación de chat
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatenlinea',  # Nombre de la base de datos
        'USER': 'chatenlinea_user',  # Usuario
        'PASSWORD': 'J5HYJYQFbA5rhTBK26CsxIaCVxDw19Oo',  # Contraseña
        'HOST': 'dpg-crr39vdds78s73cpvpr0-a',  # Hostname
        'PORT': '5432',  # Puerto
    }
}

ASGI_APPLICATION = 'chatear_amigos.asgi.application'

# Hacer que Redis sea opcional, con un chequeo antes de su configuración
if os.getenv('REDIS_URL'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.getenv('REDIS_URL')],
            },
        },
    }
else:
    print("Redis no está configurado. Funcionando sin WebSockets.")

STATIC_URL = '/static/'

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'chat_home'
LOGOUT_REDIRECT_URL = 'login'

ROOT_URLCONF = 'chatear_amigos.urls'
