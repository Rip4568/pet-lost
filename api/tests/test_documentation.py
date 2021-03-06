import pytest
from django.test import Client


class TestDocumentation:

    @pytest.fixture
    def client(self):
        client = Client()
        return client

    def test_redoc_response(self, client):
        response = client.get('/redoc/', secure=True)
        assert response.status_code == 200

    def test_swagger_response(self, client):
        response = client.get('/swagger/', secure=True)
        assert response.status_code == 200
