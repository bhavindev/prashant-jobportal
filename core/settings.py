from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def load_env():
    env_file = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split('=')
                    os.environ[key] = value

# Load environment variables from the .env file
load_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v3fu=+lkd&nirl96i@#5l*(xo0l+q%winlojg+gw4rn5d=3grt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',
    'ckeditor',
    'apps.lang',
    'apps.settings',
    'apps.homepage',
    'apps.aboutpage',
    'apps.portfoliopage',
    'apps.pricingpage',
    'apps.servicepage',
    'apps.blog',
    'apps.contactpage',
    'apps.adminapp',
    'apps.crm',
    'apps.hrm',
    'apps.userapp',
    'apps.legals',
    'apps.authapp',
    'apps.reports',
    'apps.marketing',
    'apps.custompage',
    'apps.order',
    'apps.ai',
    'apps.analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.middleware.SlugDecodeMiddleware',
]

if os.getenv('DEMO_MODE') == 'True':
    MIDDLEWARE.append('core.middleware.middleware.DemoModeMiddleware')

if os.getenv("WHITENOISE_CONFIG") == "True":
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.website_settings_context',
                'core.context_processors.promo_banner_context',
                'core.context_processors.seo_settings_context',
                'core.context_processors.menu_context',
                'core.context_processors.header_footer_context',
                'core.context_processors.user_profile_context',
                'core.context_processors.project_context',
                'core.context_processors.service_context',
                'core.context_processors.unsolved_tickets_context',
                'core.context_processors.demo_mode_enabled',
                'core.context_processors.notification_context',
                'core.context_processors.language_context',
                'apps.order.order_context.user_cart_context',
                'apps.settings.payment_method_context.payment_method_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('MYSQL_DB') == 'True' and os.getenv('POSTGRES_DB') == 'False':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DB_NAME'),
            'USER': os.getenv('MYSQL_DB_USER'),
            'PASSWORD': os.getenv('MYSQL_DB_PASSWORD'),
            'HOST': os.getenv('MYSQL_DB_HOST'),
            'PORT': os.getenv('MYSQL_DB_PORT'),
        }
    }
elif os.getenv('POSTGRES_DB') == 'True' and os.getenv('MYSQL_DB') == 'False':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB_NAME'),
            'USER': os.getenv('POSTGRES_DB_USER'),
            'PASSWORD': os.getenv('POSTGRES_DB_PASSWORD'),
            'HOST': os.getenv('POSTGRES_DB_HOST'), 
            'PORT': os.getenv('POSTGRES_DB_PORT'), 
        }
    }
    print(DATABASES)
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
            }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE')

print(f"TIME_ZONE is set to: {TIME_ZONE}")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, str(os.getenv('MEDIA_ROOT')))

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user models

AUTH_USER_MODEL = 'authapp.User'

CKEDITOR_CONFIGS = {
    'default': {
        'height': '100%',
        'width': '100%',
    },
}


# white noise settings
if os.getenv('WHITENOISE_CONFIG') == 'True':
    STORAGES = {
         "staticfiles": {
              "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
         },
    }
    
    
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

ENABLE_ARABIC_SIGNALS = False
ENABLE_BANGLA_SIGNALS = False