# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
# Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from django.conf.global_settings import gettext_noop as _

from .base_bk import *  # noqa

# Apply pymysql patch
import pymysql
pymysql.install_as_MySQLdb()
# Patch version info to forcely pass Django client check
setattr(pymysql, 'version_info', (1, 2, 6, "final", 0))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jllc(^rzpe8_udv)oadny2j3ym#qd^x^3ns11_8kq(1rf8qpd2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django_extensions',

    'backend.accounts',
    'backend.activity_log.ActivaityLogConfig',
    'backend.apps.datalog.DataLogConfig',
    'backend.apps.projects',
    'backend.apps.depot',
    'backend.apps.cluster',
    'backend.apps.configuration',
    'backend.apps.instance',
    'backend.apps.resource',
    'backend.apps.network',
    'backend.apps.metric',
    'backend.apps.variable',
    'backend.apps.ticket',
    'backend.apps.paas_monitor',
    'backend.bcs_k8s.app',
    'backend.bcs_k8s.helm',
    'backend.bcs_k8s.authtoken',
]

MIDDLEWARE = [
    'backend.accounts.middlewares.RequestProvider',

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # admin static file
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'backend/web_console/templates'),
            os.path.join(BASE_DIR, 'backend/static'),
            os.path.join(BASE_DIR, 'frontend/output'),
            os.path.join(BASE_DIR, 'staticfiles'),
            os.path.join(BASE_DIR, 'backend/apps/configuration/yaml_mode/manifests')

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': "{{%s}}",
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.apps.context_processors.global_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
LANGUAGE_COOKIE_NAME = 'blueking_language'
LANGUAGES = [
    ('zh-hans', _('中文')),
    ('en', _('English')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'backend/web_console/static/'),
    os.path.join(BASE_DIR, 'backend/static'),
    os.path.join(BASE_DIR, 'frontend/output'),
]


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'backend.utils.views.custom_exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # 'backend.utils.renderers.BKAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S"
}

# Change default cookie names to avoid conflict
SESSION_COOKIE_NAME = 'backend_sessionid'
CSRF_COOKIE_NAME = 'backend_csrftoken'
LANGUAGE_COOKIE_NAME = 'backend_dj_language'
# log max bytes：500m
LOG_MAX_BYTES = 500 * 1024 * 1024
# log count: 10
LOG_BACKUP_COUNT = 10


def get_logging_config(log_level, rds_hander_settings=None, log_path="app.log"):
    if not rds_hander_settings:
        rds_hander_settings = {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        }

    rds_hander_settings['filters'] = ["request_id"]

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s [%(asctime)s] [%(request_id)s] %(name)s %(pathname)s %(lineno)d %(funcName)s %(process)d %(thread)d \n \t %(message)s \n',  # noqa
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        "filters": {
            "request_id": {
                "()": "backend.utils.log.RequestIdFilter"
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            "file": {
                "class": "logging.handlers.WatchedFileHandler",
                "level": "DEBUG",
                "formatter": "verbose",
                "filename": log_path,
                "filters": ["request_id"]
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
                "filters": ["request_id"]
            },
            'logstash_redis': rds_hander_settings,
            'sentry': {
                'level': 'DEBUG',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'dsn': SENTRY_DSN
            }
        },
        'loggers': {
            'django': {
                'handlers': ['null'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': 'INFO',
                'propagate': True,
            },
            'django.security': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': 'INFO',
                'propagate': True
            },
            'root': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': log_level,
                'propagate': False,
            },
            'console': {  # 打印redis日志错误，防止循环错误
                'handlers': ['console', 'file'],
                'level': log_level,
                'propagate': False,
            },
            'backend': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': os.getenv('DJANGO_LOG_LEVEL', log_level),
            },
            'requests': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            },
            'bkpaas_auth': {
                'handlers': ['console', 'logstash_redis', 'file'],
                'level': 'DEBUG',
            },
            'sentry_logger': {
                'handlers': ['sentry'],
                'level': 'ERROR'
            }
        }
    }


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# request_id的头
REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'


# ******************************** Helm Config Begin ********************************
HELM_BIN = "/bin/helm"  # helm bin filename
KUBECTL_BIN = "/bin/kubectl"  # default kubectl bin filename
DASHBOARD_CTL_BIN = "/bin/dashboard-ctl"  # default dashboard ctl filename
KUBECTL_BIN_MAP = {
    "1.8.3": "/bin/kubectl",
    "1.12.3": "/bin/kubectl-v1.12.3",
    "1.14.9": "/bin/kubectl-v1.14.9"
}
KUBECFG = "/root/.kube/config"  # kubectl config path, ex: ~/.kube/config
BKE_SERVER_HOST = None  # example: http://127.0.0.1:44321
FORCE_APPLY_CLUSTER_ID = ""  # 强制将资源应用该集群，仅用于开发测试目的, 比如 localkube
KUBECTL_MAX_VISIBLE_LEVEL = 2
HELM_INSECURE_SKIP_TLS_VERIFY = False

DEFAULT_CURATOR_CHART = {
    'name': 'chartmuseum-curator',
    'version': '0.9.1',
}

HELM_NEED_REGIST_TO_BKE_WHEN_INIT = False
HELM_HAS_ABILITY_SUPPLY_CHART_REPO_SERVICE = False
# *********************************** Helm Config End *****************************

# 项目地址
DEVOPS_HOST = ''
# 容器服务地址
DEVOPS_BCS_HOST = ''
# 容器服务 API 地址
DEVOPS_BCS_API_URL = ''
# 仓库地址
DEVOPS_ARTIFACTORY_HOST = ''
RUN_ENV = 'dev'

BK_KIND_LIST = [1, 2]
BK_CC_HOST = ''

SITE_URL = '/'

BK_IAM_APP_URL = ''

THANOS_HOST = ''
# 默认指标数据来源，现在支持bk-data, prometheus
DEFAULT_METRIC_SOURCE = "bk-data"
# 普罗米修斯项目白名单
DEFAULT_METRIC_SOURCE_PROM_WLIST = []

# web_console运行模式, 支持external(平台托管), internal（自己集群托管）
WEB_CONSOLE_MODE = 'external'

# web_console kubectld命令
WEB_CONSOLE_KUBECTLD_IMAGE_PATH = ''
WEB_CONSOLE_POD_SPEC = {}
WEB_CONSOLE_PORT = int(os.environ.get('WEB_CONSOLE_PORT', 28800))

# 灰度功能提示消息
GRAYSCALE_FEATURE_MSG = "功能灰度测试中，请联系管理员添加白名单"

# 覆盖配置
try:
    from .base_bk import DATABASE_ROUTERS, TEMPLATES, STATICFILES_DIRS
except Exception:
    pass
