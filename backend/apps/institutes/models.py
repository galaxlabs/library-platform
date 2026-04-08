from django.db import models

from apps.common.models import BaseModel


class Institute(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    admin = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_institutes',
    )
    policies = models.JSONField(default=dict)
    branding = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class ClassDarjah(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='classes',
    )
    level = models.IntegerField(default=1)
    order_index = models.IntegerField(default=0)
    language_pair = models.CharField(
        max_length=50,
        choices=[
            ('ar-ur', 'Arabic + Urdu'),
            ('ar-en', 'Arabic + English'),
        ],
        default='ar-en',
    )
    metadata = models.JSONField(default=dict)

    class Meta:
        unique_together = [('institute', 'name')]

    def __str__(self):
        return f'{self.institute.name} - {self.name}'


class Subject(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    arabic_name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class InstituteMembership(BaseModel):
    ROLE_CHOICES = [
        ('platform_admin', 'Platform Admin'),
        ('institute_admin', 'Institute Admin'),
        ('scholar', 'Scholar'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('reviewer', 'Reviewer'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='institute_memberships',
    )
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    class_darjah = models.ForeignKey(
        ClassDarjah,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memberships',
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('user', 'institute', 'role')]


class InstituteSubject(BaseModel):
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='subject_offerings',
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='institute_offerings',
    )
    class_darjah = models.ForeignKey(
        ClassDarjah,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subject_offerings',
    )
    curriculum_metadata = models.JSONField(default=dict)
    is_required = models.BooleanField(default=False)


class InstitutePrivateLibraryAccess(BaseModel):
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        related_name='private_library_access_entries',
    )
    book = models.ForeignKey(
        'library.Book',
        on_delete=models.CASCADE,
        related_name='institute_access_entries',
    )
    access_level = models.CharField(
        max_length=30,
        choices=[
            ('view', 'View'),
            ('study', 'Study'),
            ('manage', 'Manage'),
        ],
        default='view',
    )
    is_active = models.BooleanField(default=True)
