from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('RM', 'Remote'),
    )

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    experience = models.PositiveIntegerField(help_text="Experience in years")
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    domain = models.CharField(max_length=150, help_text="Eg: Web Development, Data Science")
    skills = models.TextField(help_text="Comma separated skills")
    description = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')


from django.db import models

class Application(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
    )

    MEETING_STATUS_CHOICES = (
        ('NOT_SCHEDULED', 'Not Scheduled'),
        ('SCHEDULED', 'Scheduled'),
        ('POSTPONED', 'Postponed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='applications/resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    meeting_status = models.CharField(max_length=20, choices=MEETING_STATUS_CHOICES, default='NOT_SCHEDULED')
    meeting_datetime = models.DateTimeField(null=True, blank=True)  # NEW

    class Meta:
        unique_together = ('user', 'job')

# Query Models
from django.db import models
from django.conf import settings

class JobQuery(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='queries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # candidate
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Query by {self.user.email} on {self.job.title}"


class JobQueryReply(models.Model):
    query = models.ForeignKey(JobQuery, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # can be candidate or consultant
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.user.email} on Query {self.query.id}"


