# pytest configuration
import os

import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
os.environ.setdefault('PYTEST_CURRENT_TEST', '1')

django.setup()


@pytest.fixture(autouse=True)
def _temp_media_root(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / 'media'
