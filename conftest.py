import os
import django
from django.conf import settings

def pytest_configure():
    """Configure Django settings before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_project.settings')
    django.setup()
