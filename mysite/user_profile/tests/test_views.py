import pytest
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from turnstile.fields import TurnstileField


@pytest.mark.django_db
class TestAuthentification:
    
    def test_registration(self, client):
        """Проверка: регистрация."""
        data = {
            'username': 'testuser11',
            'email': 'testuser@example.com',
            'password1': 'strong_password_123',
            'password2': 'strong_password_123',
            'cf-turnstile-response': 'mocked-token-value',
        }
        url = reverse('user_profile:registration') 
        response = client.post(url, data=data)
        
        assert User.objects.filter(email='testuser@example.com').exists()