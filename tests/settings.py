
"""
Django settings for running tests
"""

SECRET_KEY = 'secret'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_troll',
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

ROOT_URLCONF = 'tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]