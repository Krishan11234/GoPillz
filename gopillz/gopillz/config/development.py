DATABASES = {}

if DEV_DATABASE:
    DATABASES['default']= {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gopillz',
        'USER': '',
        'PASSWORD': '<password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
else:
    DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'gopillz',
    'USER': '',
    'PASSWORD': '<password>',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    }