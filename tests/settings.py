
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