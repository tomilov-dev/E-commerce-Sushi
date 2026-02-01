import os
from pathlib import Path
from dotenv import load_dotenv

## Environment Checkout
load_dotenv()
check_env = os.getenv("ENV_CHECK")
if not check_env:
    raise FileNotFoundError(".env file not found")

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
    BASE_DIR / "components",
]


DELIVERY_PRICES = {
    0: 150,  ## if Price <2500 Then DP = 150
    2500: 100,  ## If Price >= 2500 Then DP = 100
    5000: 0,  ## If Price >= 5000 Then DP = 0
}

CART_SESSION_ID = "cart"
PHONE_HASH_SESSION_ID = "PHONE_HASH"
RESEND_TIMER_SESSION_ID = "RESEND_TIMER"

AUTH_USER_MODEL = "accounts.CustomUser"

SESSION_COOKIE_AGE = 86400

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")


debug_mode = os.getenv("DJANGO_DEBUG")
if debug_mode == "True":
    DEBUG = True
elif debug_mode == "False":
    DEBUG = False
else:
    raise ValueError("DJANGO_DEBUG has wrong value")


ALLOWED_HOSTS = [
    "tomilov.space",
    "delivery-mpa.tomilov.space",
    "delivery.itomilov.tech",
]

if DEBUG:
    ALLOWED_HOSTS.append("localhost")
    ALLOWED_HOSTS.append("127.0.0.1")

INTERNAL_IPS = [
    "127.0.0.1",
]

RD_USER = os.getenv("REDIS_USER")
RD_PASS = os.getenv("REDIS_PASSWORD")
RD_HOST = os.getenv("REDIS_HOST")
RD_PORT = os.getenv("REDIS_PORT")

if DEBUG:
    ### Use MemCache in dev-mode
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
else:
    ### Use Redis Cache in production
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://{RD_USER}:{RD_PASS}@{RD_HOST}:{RD_PORT}",
            "OPTIONS": {
                "db": "10",
            },
        }
    }

AUTHENTICATION_BACKENDS = [
    "accounts.auth_backend.CustomPhoneAuthBackend",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    ## Projects Apps
    "products.apps.ProductsConfig",
    "promotion.apps.PromotionConfig",
    "categories.apps.CategoriesConfig",
    "tags.apps.TagsConfig",
    "pages.apps.PagesConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "accounts.apps.AccountsConfig",
    "online_payment.apps.OnlinePaymentConfig",
    ## Dev Modules
    # "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ## Additional Modules
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
            "components",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                ## app context
                "categories.context_processors.categories_context",
                "promotion.context_processors.promotion_context",
                "cart.context_processors.cart_context",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "NAME": os.getenv("POSTGRES_NAME", "delivery_mpa"),
        "USER": os.getenv("POSTGRES_USER", "admin"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING = {
#     "version": 1,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "loggers": {
#         "django.db.backends": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#         }
#     },
# }
