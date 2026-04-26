import os
import django
from django.conf import settings
import pytest

def pytest_configure():
    """Configure Django settings before running tests."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    django.setup()

@pytest.fixture(autouse=True)
def clear_database_before_each_test(db):
    """Clear database before each test."""
    from django_project.category_app.models import Category
    Category.objects.all().delete()
    yield
    Category.objects.all().delete()
