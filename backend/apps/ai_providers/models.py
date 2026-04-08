from abc import ABC, abstractmethod
from django.db import models
from django.contrib.postgres.fields import ArrayField
from cryptography.fernet import Fernet
import os

from apps.common.models import BaseModel


class AIProvider(BaseModel):
    """
    Store AI provider configurations and credentials.
    Supports system, institute, and user-level keys.
    """
    PROVIDER_CHOICES = [
        ('gemini', 'Google Gemini'),
        ('openrouter', 'OpenRouter'),
        ('ollama', 'Ollama (Local)'),
    ]

    SCOPE_CHOICES = [
        ('system', 'System Default'),
        ('institute', 'Institute Level'),
        ('user', 'User Personal'),
    ]

    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='system')
    
    # Encrypted API keys
    api_key = models.TextField()
    
    # For Ollama and local deployments
    base_url = models.URLField(null=True, blank=True, help_text='e.g., http://localhost:11434 for Ollama')
    model_name = models.CharField(max_length=100, null=True, blank=True, help_text='Model identifier for the provider')
    
    # Scope relationships
    institute = models.ForeignKey(
        'institutes.Institute',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_providers'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_providers'
    )
    
    # Status and settings
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text='Higher priority used first')
    rate_limit = models.IntegerField(default=0, help_text='Requests per minute (0=unlimited)')
    timeout_seconds = models.IntegerField(default=30)
    
    # Configuration (JSON)
    config = models.JSONField(default=dict, blank=True, help_text='Provider-specific settings')
    
    class Meta:
        unique_together = [('name', 'scope', 'institute', 'user')]
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return f'{self.get_name_display()} ({self.get_scope_display()})'
    
    def decrypt_key(self):
        """Decrypt and return the API key."""
        cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY').encode())
        return cipher_suite.decrypt(self.api_key.encode()).decode()
    
    def encrypt_key(self, key):
        """Encrypt and store the API key."""
        cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY').encode())
        self.api_key = cipher_suite.encrypt(key.encode()).decode()


class ProviderAdapterBase(ABC):
    """
    Abstract base class for AI provider adapters.
    All provider-specific implementations must extend this.
    """

    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.api_key = provider.decrypt_key()
        self.model_name = provider.model_name
        self.base_url = provider.base_url
        self.config = provider.config
        self.timeout = provider.timeout_seconds

    @abstractmethod
    async def query(self, prompt: str, context: dict = None) -> dict:
        """
        Query the provider with a prompt.
        
        Returns:
        {
            'response': str,
            'model': str,
            'tokens_used': int,
            'provider': str,
        }
        """
        pass

    @abstractmethod
    async def embed(self, text: str) -> list:
        """Generate embeddings for text."""
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Check if provider is accessible and healthy."""
        pass


class GeminiAdapter(ProviderAdapterBase):
    """Adapter for Google Gemini API."""

    async def query(self, prompt: str, context: dict = None) -> dict:
        """Query Gemini API."""
        # Implementation in separate file or imported from service
        pass

    async def embed(self, text: str) -> list:
        """Generate embeddings via Gemini."""
        pass

    async def is_healthy(self) -> bool:
        """Check Gemini API health."""
        pass


class OpenRouterAdapter(ProviderAdapterBase):
    """Adapter for OpenRouter API."""

    async def query(self, prompt: str, context: dict = None) -> dict:
        """Query OpenRouter API."""
        pass

    async def embed(self, text: str) -> list:
        """Generate embeddings via OpenRouter."""
        pass

    async def is_healthy(self) -> bool:
        """Check OpenRouter API health."""
        pass


class OllamaAdapter(ProviderAdapterBase):
    """Adapter for Ollama local deployment."""

    async def query(self, prompt: str, context: dict = None) -> dict:
        """Query local Ollama instance."""
        pass

    async def embed(self, text: str) -> list:
        """Generate embeddings via Ollama."""
        pass

    async def is_healthy(self) -> bool:
        """Check Ollama instance health."""
        pass


def get_adapter(provider_name: str, scope: str = 'system', institute_id=None, user_id=None) -> ProviderAdapterBase:
    """
    Factory function to get adapter for a provider.
    Follows hierarchy: User > Institute > System.
    """
    provider = None
    
    # Try user scope first (if user_id provided)
    if user_id:
        provider = AIProvider.objects.filter(
            name=provider_name,
            scope='user',
            user_id=user_id,
            is_active=True
        ).first()
    
    # Then try institute scope
    if not provider and institute_id:
        provider = AIProvider.objects.filter(
            name=provider_name,
            scope='institute',
            institute_id=institute_id,
            is_active=True
        ).first()
    
    # Then system default
    if not provider:
        provider = AIProvider.objects.filter(
            name=provider_name,
            scope='system',
            is_active=True
        ).first()
    
    if not provider:
        raise ValueError(f'No active provider found for {provider_name}')
    
    # Map provider name to adapter class
    adapters = {
        'gemini': GeminiAdapter,
        'openrouter': OpenRouterAdapter,
        'ollama': OllamaAdapter,
    }
    
    adapter_class = adapters.get(provider_name)
    if not adapter_class:
        raise ValueError(f'Unknown provider: {provider_name}')
    
    return adapter_class(provider)