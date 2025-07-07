import os
from pathlib import Path

# Django settings for the authentication system
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_app',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

AUTH_USER_MODEL = 'auth_app.CustomUser'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CORS_ALLOW_ALL_ORIGINS = True

# ✅ SendGrid SMTP Email Configuration (no .env, directly in settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # DO NOT change this
EMAIL_HOST_PASSWORD = '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'  # ⚠️ Replace with your real SendGrid API key
DEFAULT_FROM_EMAIL = 'kingisright67@gmail.com'  # This must be verified in SendGrid

# 🔧 Stage-wise responsible person email mapping
SENDGRID_API_KEY = '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' 
SENDER_EMAIL = 'kingisright67@gmail.com'
STAGE_EMAILS = {
    'Material': 'yashbharvada4@gmail.com',
    'Manufacturing': 'gabanidj@gmail.com',
    'Packaging': 'princediyora05@gmail.com',
    'Dispatch': 'krrishmiraj12345@gmail.com',
    'Completed': 'kingisright67@gmail.com',
}
