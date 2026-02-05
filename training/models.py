from django.db import models
from django.conf import settings
from django.utils import timezone

def certificate_upload_path(instance, filename):
    return f"certificates/user_{instance.candidate.user.id}/{filename}"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    candidate = models.ForeignKey(
        'profiles.CandidateProfile', on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    applied_at = models.DateTimeField(default=timezone.now)
    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    certificate = models.FileField(
        upload_to=certificate_upload_path, null=True, blank=True
    )

    class Meta:
        unique_together = ('candidate', 'course')

    def __str__(self):
        return f"{self.candidate.user.email} - {self.course.title}"
