LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'saas',
        'HOST': '129.28.179.236',
        'PORT': 3306,
        'USER': 'chao',
        'PASSWORD': 'chao',
    }
}


CACHES = {
    "default": { # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://129.28.179.236:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}


TENCENT_SMS_APP_ID = 1400440898  # 自己应用ID
TENCENT_SMS_APP_KEY = "afb27e4602ef5543080432a497fb6ec5"  # 自己应用Key
TENCENT_SMS_APP_SIGN = "朕只是抬抬手公众号"

TENCENT_COS_ID = ''
TENCENT_COS_KEY = ''
