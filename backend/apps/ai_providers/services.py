from __future__ import annotations

import os
from dataclasses import dataclass

import requests
from requests import RequestException

from .models import AIProvider


class ProviderError(Exception):
    pass


@dataclass
class ResolvedProvider:
    provider_type: str
    scope: str
    api_key: str
    base_url: str | None
    model_name: str | None
    timeout_seconds: int
    config: dict
    db_provider: AIProvider | None = None


class BaseProviderAdapter:
    def __init__(self, provider: ResolvedProvider):
        self.provider = provider
        self.timeout = provider.timeout_seconds

    def query(self, prompt: str, context: dict | None = None) -> dict:
        raise NotImplementedError

    def embed(self, text: str) -> dict:
        raise NotImplementedError

    def health_check(self) -> dict:
        raise NotImplementedError

    def _wrap_request_error(self, exc: Exception) -> ProviderError:
        if isinstance(exc, RequestException):
            return ProviderError(f'{self.provider.provider_type} request failed: {exc.__class__.__name__}')
        return ProviderError(str(exc))


class GeminiAdapter(BaseProviderAdapter):
    def _url(self, suffix: str):
        base = self.provider.base_url or 'https://generativelanguage.googleapis.com/v1beta'
        return f'{base}{suffix}'

    def query(self, prompt: str, context: dict | None = None) -> dict:
        url = self._url(f'/models/{self.provider.model_name or "gemini-1.5-flash"}:generateContent')
        try:
            response = requests.post(
                url,
                params={'key': self.provider.api_key},
                json={'contents': [{'parts': [{'text': prompt}]}]},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        text = ''
        candidates = data.get('candidates') or []
        if candidates:
            parts = candidates[0].get('content', {}).get('parts', [])
            text = '\n'.join(part.get('text', '') for part in parts if part.get('text'))
        return {
            'response': text,
            'provider': 'gemini',
            'model': self.provider.model_name or 'gemini-1.5-flash',
            'raw': data,
        }

    def embed(self, text: str) -> dict:
        url = self._url('/models/text-embedding-004:embedContent')
        try:
            response = requests.post(
                url,
                params={'key': self.provider.api_key},
                json={'content': {'parts': [{'text': text}]}},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        return {'embedding': data.get('embedding', {}).get('values', []), 'raw': data}

    def health_check(self) -> dict:
        try:
            result = self.query('Respond with: OK')
            return {'healthy': bool(result['response']), 'provider': 'gemini'}
        except Exception as exc:
            return {'healthy': False, 'provider': 'gemini', 'error': exc.__class__.__name__}


class OpenRouterAdapter(BaseProviderAdapter):
    def _headers(self):
        return {
            'Authorization': f'Bearer {self.provider.api_key}',
            'Content-Type': 'application/json',
        }

    def query(self, prompt: str, context: dict | None = None) -> dict:
        url = f'{self.provider.base_url or "https://openrouter.ai/api/v1"}/chat/completions'
        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json={
                    'model': self.provider.model_name or 'openai/gpt-4o-mini',
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        choices = data.get('choices') or []
        text = choices[0].get('message', {}).get('content', '') if choices else ''
        return {
            'response': text,
            'provider': 'openrouter',
            'model': self.provider.model_name or 'openai/gpt-4o-mini',
            'raw': data,
        }

    def embed(self, text: str) -> dict:
        url = f'{self.provider.base_url or "https://openrouter.ai/api/v1"}/embeddings'
        try:
            response = requests.post(
                url,
                headers=self._headers(),
                json={
                    'model': self.provider.model_name or 'text-embedding-3-small',
                    'input': text,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        embedding = data.get('data', [{}])[0].get('embedding', [])
        return {'embedding': embedding, 'raw': data}

    def health_check(self) -> dict:
        try:
            result = self.query('Respond with: OK')
            return {'healthy': bool(result['response']), 'provider': 'openrouter'}
        except Exception as exc:
            return {'healthy': False, 'provider': 'openrouter', 'error': exc.__class__.__name__}


class OllamaAdapter(BaseProviderAdapter):
    def query(self, prompt: str, context: dict | None = None) -> dict:
        url = f'{self.provider.base_url or "http://127.0.0.1:11434"}/api/generate'
        try:
            response = requests.post(
                url,
                json={
                    'model': self.provider.model_name or 'llama3.1',
                    'prompt': prompt,
                    'stream': False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        return {
            'response': data.get('response', ''),
            'provider': 'ollama',
            'model': self.provider.model_name or 'llama3.1',
            'raw': data,
        }

    def embed(self, text: str) -> dict:
        url = f'{self.provider.base_url or "http://127.0.0.1:11434"}/api/embeddings'
        try:
            response = requests.post(
                url,
                json={'model': self.provider.model_name or 'nomic-embed-text', 'prompt': text},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise self._wrap_request_error(exc) from exc
        return {'embedding': data.get('embedding', []), 'raw': data}

    def health_check(self) -> dict:
        try:
            response = requests.get(
                f'{self.provider.base_url or "http://127.0.0.1:11434"}/api/tags',
                timeout=self.timeout,
            )
            response.raise_for_status()
            return {'healthy': True, 'provider': 'ollama'}
        except Exception as exc:
            return {'healthy': False, 'provider': 'ollama', 'error': exc.__class__.__name__}


ADAPTERS = {
    'gemini': GeminiAdapter,
    'openrouter': OpenRouterAdapter,
    'ollama': OllamaAdapter,
}


def _env_provider(provider_name: str) -> ResolvedProvider | None:
    mapping = {
        'gemini': {
            'api_key': os.getenv('GEMINI_API_KEY', ''),
            'base_url': os.getenv('GEMINI_BASE_URL', ''),
            'model_name': os.getenv('GEMINI_MODEL', 'gemini-1.5-flash'),
        },
        'openrouter': {
            'api_key': os.getenv('OPENROUTER_API_KEY', ''),
            'base_url': os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1'),
            'model_name': os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o-mini'),
        },
        'ollama': {
            'api_key': '',
            'base_url': os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434'),
            'model_name': os.getenv('OLLAMA_MODEL', 'llama3.1'),
        },
    }
    config = mapping.get(provider_name)
    if not config:
        return None
    if provider_name != 'ollama' and not config['api_key']:
        return None
    return ResolvedProvider(
        provider_type=provider_name,
        scope='system',
        api_key=config['api_key'],
        base_url=config['base_url'] or None,
        model_name=config['model_name'],
        timeout_seconds=int(os.getenv('AI_PROVIDER_TIMEOUT', '30')),
        config={},
    )


def resolve_provider(provider_name: str, *, user=None, institute=None) -> ResolvedProvider:
    queryset = AIProvider.objects.filter(name=provider_name, is_active=True)
    candidates = []
    if user is not None:
        candidates.extend(queryset.filter(scope='user', user=user).order_by('-priority')[:1])
    if institute is not None:
        candidates.extend(queryset.filter(scope='institute', institute=institute).order_by('-priority')[:1])
    candidates.extend(queryset.filter(scope='system').order_by('-priority')[:1])

    if candidates:
        provider = candidates[0]
        return ResolvedProvider(
            provider_type=provider.name,
            scope=provider.scope,
            api_key=provider.decrypt_key(),
            base_url=provider.base_url,
            model_name=provider.model_name,
            timeout_seconds=provider.timeout_seconds,
            config=provider.config,
            db_provider=provider,
        )

    env_provider = _env_provider(provider_name)
    if env_provider:
        return env_provider
    raise ProviderError(f'No provider configuration found for {provider_name}')


def get_adapter(provider_name: str, *, user=None, institute=None):
    provider = resolve_provider(provider_name, user=user, institute=institute)
    adapter_class = ADAPTERS.get(provider.provider_type)
    if not adapter_class:
        raise ProviderError(f'Unknown provider {provider.provider_type}')
    return adapter_class(provider)
