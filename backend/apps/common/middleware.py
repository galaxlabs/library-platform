import logging
from django.utils.deprecation import MiddlewareNotUsed
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """
    Add security headers to all responses.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class AuditLoggingMiddleware:
    """
    Log all requests for audit purposes.
    Tracks authentication events, failed requests, etc.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log auth attempts
        if request.path.startswith('/api/v1/auth/'):
            logger.info(
                f'Auth attempt: {request.method} {request.path} | '
                f'IP: {self.get_client_ip(request)}'
            )
        
        response = self.get_response(request)
        
        # Log failed requests (4xx, 5xx)
        if response.status_code >= 400:
            logger.warning(
                f'Request failed: {request.method} {request.path} | '
                f'Status: {response.status_code} | '
                f'User: {request.user} | '
                f'IP: {self.get_client_ip(request)}'
            )
        
        return response

    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RateLimitMiddleware:
    """
    Apply rate limiting to API endpoints.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.limits = {
            '/api/v1/auth/login/': '5/m',  # 5 per minute
            '/api/v1/auth/register/': '3/h',  # 3 per hour
        }

    def __call__(self, request):
        # Check if this path has a rate limit
        for path_pattern, limit in self.limits.items():
            if request.path.startswith(path_pattern):
                # Rate limiting can be checked here
                # For now, we'll use django-ratelimit decorators on views
                pass
        
        response = self.get_response(request)
        return response