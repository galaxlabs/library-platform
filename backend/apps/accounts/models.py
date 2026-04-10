from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from .managers import CustomUserManager


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=255)
    arabic_name = models.CharField(max_length=255, blank=True)
    roles = models.ManyToManyField(Role, related_name='users')
    preferred_lang_pair = models.CharField(
        max_length=50,
        choices=[
            ('ar-ur', 'Arabic + Urdu'),
            ('ar-en', 'Arabic + English'),
        ],
        default='ar-en'
    )
    institute = models.ForeignKey(
        'institutes.Institute',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    class_darjah = models.ForeignKey(
        'institutes.ClassDarjah',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name or self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
