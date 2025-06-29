import pytest

@pytest.fixture(autouse=True)
def setup_django():
    import django
    from django.conf import settings

    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'task_manager',
            ],
            MIDDLEWARE_CLASSES=(),
        )
        django.setup()