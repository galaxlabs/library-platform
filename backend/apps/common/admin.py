from django.contrib import admin
from .audit import AuditLog, PermissionGrant

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource_type', 'created_at', 'success']
    list_filter = ['action', 'success', 'created_at']
    search_fields = ['user__username', 'resource_type']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

@admin.register(PermissionGrant)
class PermissionGrantAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission', 'granted_by', 'is_active']
    list_filter = ['permission', 'granted_at']
    search_fields = ['user__username', 'permission']
