from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('arabic_name', 'phone', 'preferred_lang_pair', 'institute', 'class_darjah')}),
        ('Roles', {'fields': ('roles',)}),
    )
    list_display = ['email', 'full_name', 'institute', 'is_staff', 'is_active']
    search_fields = ['email', 'full_name', 'arabic_name']
    filter_horizontal = ['roles', 'groups', 'user_permissions']
