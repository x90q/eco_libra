from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'SECRET_KEY', 
    default='django-insecure-test-key-for-local-development-only'
)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


# Application definition

SITE_ID = 2

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',


    # messages
    'django.contrib.messages',

    # db
    'django.contrib.postgres',

    # tags
    'taggit',

    # my apps
    'feed.apps.FeedConfig',
    'members.apps.MembersConfig',
    'search.apps.SearchConfig',
    'account_management.apps.AccountManagementConfig',

    # runserver_plus
    'django_extensions',

    # allauth
    'allauth',
    'allauth.account',

    # auth (required for all auth)
    'django.contrib.auth',

    # allauth social login
    'allauth.socialaccount',

    #allauth google oauth
    'allauth.socialaccount.providers.google',

    # ui design
    'tailwind',
    'theme',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # allauth
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'eco_libra_base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'feed.context_processors.categories_processor',
            ],
        },
    },
]

# auth logic

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_SIGNUP_FIELDS = [
    'username*', 'email*', 'password1*', 'password2*'
]

ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = 'phone'

ACCOUNT_LOGIN_BY_CODE_ENABLED = True

ALLAUTH_USER_CODE_FORMAT =  {
    "numeric": False,
    "dashed": True,
    "length": 8
    }

ACCOUNT_LOGIN_BY_CODE_MAX_ATTEMPTS = 2

ACCOUNT_LOGIN_BY_CODE_SUPPORTS_RESEND = True

ACCOUNT_LOGIN_BY_CODE_TIMEOUT = 180

ACCOUNT_LOGIN_METHODS = {"username", "email"}

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'members:my_profile'

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

ACCOUNT_LOGIN_TIMEOUT = 420

ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 2

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_EMAIL_NOTIFICATIONS = True

ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False

ACCOUNT_CHANGE_EMAIL = True

ACCOUNT_USERNAME_BLACKLIST = []

ACCOUNT_USERNAME_MIN_LENGTH = 3

ACCOUNT_USERNAME_VALIDATORS = "account_management.validators.custom_username_validators"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': config('GOOGLE_OAUTH2_CLIENT_ID'),
            'secret':  config('GOOGLE_OAUTH2_SECRET'),
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'account_management.adapters.MySocialAccountAdapter'

LOGIN_URL = "/account/login/"

LOGIN_REDIRECT_URL = 'members:my_profile'
LOGOUT_REDIRECT_URL = 'feed:home'


WSGI_APPLICATION = 'eco_libra_base.wsgi.application'


# css 

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1", "localhost", "eco-libra.com:8000",
]

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"

# Database Configuration
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME', default='eco_libra_db'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default='postgres'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}


# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'


# Email Configuration

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'OPTIONS': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'use_tls': True,
            'username': config('EMAIL_HOST_USER', default=''),
            'password': config('EMAIL_HOST_PASSWORD', default=''),
        },
    },
}

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@localhost')

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

