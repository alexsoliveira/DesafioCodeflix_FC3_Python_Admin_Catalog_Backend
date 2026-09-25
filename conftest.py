import os
import django
import pytest
from django.conf import settings
from django.core.management import call_command

def pytest_configure():
    """Configure Django settings before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_project.settings')
    django.setup()
    call_command("migrate", run_syncdb=True, verbosity=0)


@pytest.fixture(autouse=True)
def isolate_django_db(request):
    if "django_db" in request.keywords:
        call_command("flush", verbosity=0, interactive=False)

    yield
