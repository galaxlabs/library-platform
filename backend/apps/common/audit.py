import logging
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now
from django.db import models
from apps.common.models import BaseModel

logger = logging.getLogger(__name__)


class AuditLog(BaseModel):
    """
    Track all important actions for security and compliance.
    """
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('register', 'User Registration'),
        ('upload', 'Book Upload'),
        ('delete', 'Content Deletion'),
        ('review', 'Scholar Review'),
        ('approve', 'Content Approval'),
        ('reject', 'Content Rejection'),
        ('export', 'Data Export'),
        ('admin_action', 'Admin Action'),
        ('permission_grant', 'Permission Granted'),
        ('permission_revoke', 'Permission Revoked'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100, help_text='Model name (e.g., Book, Scholar)')
    resource_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    
    # Context information
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Change tracking
    old_values = models.JSONField(null=True, blank=True, help_text='Previous state')
    new_values = models.JSONField(null=True, blank=True, help_text='New state')
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]

    def __str__(self):
        return f'{self.get_action_display()} by {self.user} on {self.created_at}'


class PermissionGrant(BaseModel):
    """
    Track custom permission grants for fine-grained access control.
    """
    PERMISSION_CHOICES = [
        ('view_institute', 'View Institute Data'),
        ('edit_institute', 'Edit Institute Data'),
        ('moderate_content', 'Moderate Content'),
        ('publish_content', 'Publish Content'),
        ('review_answers', 'Review Q&A Answers'),
        ('manage_scholars', 'Manage Scholars'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='permission_grants'
    )
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES)
    resource_type = models.CharField(max_length=100, null=True, blank=True, help_text='e.g., Institute')
    resource_id = models.IntegerField(null=True, blank=True)
    
    granted_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='permissions_granted'
    )
    granted_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Automatic expiration date')

    class Meta:
        unique_together = [('user', 'permission', 'resource_type', 'resource_id')]
        ordering = ['-granted_at']

    def __str__(self):
        return f'{self.user.username} - {self.get_permission_display()}'

    @property
    def is_active(self):
        if self.expires_at:
            return self.expires_at > now()
        return True


def log_action(
    user,
    action,
    resource_type,
    description,
    resource_id=None,
    request=None,
    success=True,
    error_message='',
    old_values=None,
    new_values=None,
):
    """
    Utility function to log an action.
    """
    ip_address = None
    user_agent = ''
    
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    AuditLog.objects.create(
        user=user,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        success=success,
        error_message=error_message,
        old_values=old_values,
        new_values=new_values,
    )
    
    logger.info(
        f'Action: {action} | User: {user} | Resource: {resource_type} | Success: {success}'
    )


def get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip