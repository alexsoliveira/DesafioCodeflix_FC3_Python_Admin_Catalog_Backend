import os
import django
from django.conf import settings
from django.core.management import call_command

def pytest_configure():
    """Configure Django settings before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_project.settings')
    django.setup()
    call_command("migrate", run_syncdb=True, verbosity=0)
