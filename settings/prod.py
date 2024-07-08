from .base import *
import dj_database_url
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['resolution-software.herokuapp.com']
# ALLOWED_HOSTS = ['*']



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


#============= STATIC & MEDIA BACKEND ================#
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#============= STATIC & MEDIA BACKEND AWS S3================#
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400 "}
PUBLIC_MEDIA_LOCATION = 'Plantillas Bases'
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = 'lista.storages.ResolutionStorage'


# lOGGING SYSTEM
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False, 
    'formatters':{
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'Simple_Format':{
            'format': '{levelname} {message}',
            'style': '{',
        }
    },
 
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            # 'class': 'logging.FileHandler',
            # 'filename': './logs/log_file1.log',
            'formatter':'Simple_Format',
        },
 
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
 
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },

}

DEBUG_PROPAGATE_EXCEPTIONS = True