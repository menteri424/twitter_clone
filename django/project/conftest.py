import pytest
from django_webtest import WebTestMixin


@pytest.fixture
def web_app(django_app_factory):
    return django_app_factory(csrf_checks=False)
