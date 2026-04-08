from django.db import models

from apps.common.models import BaseModel


class Scholar(BaseModel):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='scholar_profile',
    )
    full_name = models.CharField(max_length=255, blank=True)
    arabic_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    madrasa_or_institute = models.CharField(max_length=255, blank=True)
    darjah_or_final_year = models.CharField(max_length=100, blank=True)
    sanad_or_ijazah_info = models.TextField(blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    specialization_subjects = models.JSONField(default=list, blank=True)
    current_teaching_role = models.CharField(max_length=255, blank=True)
    short_bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='scholars/photos/', null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    verification_status = models.CharField(
        max_length=50,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending',
    )
    badge_status = models.CharField(max_length=50, blank=True)
    trust_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    correction_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.full_name or self.user.full_name


class ScholarCredential(BaseModel):
    scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE, related_name='credentials')
    credential_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    issuing_body = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='scholars/credentials/', null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class ScholarReview(BaseModel):
    scholar = models.ForeignKey(Scholar, on_delete=models.CASCADE, related_name='reviews')
    answer = models.ForeignKey(
        'qa_engine.Answer',
        on_delete=models.CASCADE,
        related_name='scholar_reviews',
    )
    decision = models.CharField(
        max_length=30,
        choices=[
            ('support', 'Support'),
            ('object', 'Object'),
            ('revise', 'Revise'),
        ],
    )
    commentary = models.TextField(blank=True)
    evidence_notes = models.JSONField(default=list, blank=True)


class VerifiedExplanation(BaseModel):
    answer = models.OneToOneField(
        'qa_engine.Answer',
        on_delete=models.CASCADE,
        related_name='verified_explanation',
    )
    scholar = models.ForeignKey(
        Scholar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_explanations',
    )
    explanation = models.TextField()
    status = models.CharField(max_length=30, default='published')
