from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from .validators import validate_file_size_5mb


def user_resume_path(instance, filename):
    return f"resumes/user_{instance.user.id}/{filename}"


def user_profile_image_path(instance, filename):
    return f"profile_images/user_{instance.user.id}/{filename}"


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Candidate details
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    experience_years = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )

    skills = models.TextField(blank=True, help_text="Comma-separated skills")

    resume = models.FileField(
        upload_to=user_resume_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            validate_file_size_5mb
        ],
        null=True,
        blank=True
    )

    # ✅ PROFILE IMAGE (FIXED)
    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        null=True,
        blank=True
    )

    # Optional extras
    bio = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def profile_completeness(self):
        fields = [
            self.first_name,
            self.last_name,
            self.phone,
            self.location,
            self.experience_years,
            self.skills,
            self.resume,
            self.profile_image,
            self.bio,
            self.linkedin,
            self.github
        ]
        filled = sum(bool(f) for f in fields)
        return int((filled / len(fields)) * 100)

    def __str__(self):
        return self.user.email

from django.db import models
from django.conf import settings
from django.utils import timezone

def consultant_profile_image_path(instance, filename):
    return f"consultant_profile_images/user_{instance.user.id}/{filename}"


class ConsultantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultant_profile'
    )

    # Consultant details
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(
        upload_to=consultant_profile_image_path,
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def profile_completeness(self):
        fields = [
            self.first_name,
            self.last_name,
            self.phone,
            self.company,
            self.designation,
            self.profile_image,
            self.bio,
            self.linkedin
        ]
        filled = sum(bool(f) for f in fields)
        return int((filled / len(fields)) * 100)

    def __str__(self):
        return self.user.email


# ----------------------------
# Auto-create profile
# ----------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_candidate_profile(sender, instance, created, **kwargs):
    if created:
        CandidateProfile.objects.create(user=instance)


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_consultant_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'CONSULTANT':
        ConsultantProfile.objects.create(user=instance)

