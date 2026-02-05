from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Subscription(models.Model):

    PLAN_CHOICES = (
        ('FREE', 'Free'),
        ('PRO', 'Pro'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    plan = models.CharField(
        max_length=10,
        choices=PLAN_CHOICES,
        default='FREE'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def activate_pro(self):
        """Upgrade user to PRO plan"""
        self.plan = 'PRO'
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=30)
        self.is_active = True
        self.save()

    def is_pro(self):
        """Check if subscription is currently PRO"""
        if self.plan != 'PRO':
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return True

    def __str__(self):
        return f"{self.user.email} - {self.plan}"
