from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Subscription


@receiver(post_save, sender=User)
def create_subscription_for_candidate(sender, instance, created, **kwargs):
    if created and instance.role == 'CANDIDATE':
        Subscription.objects.create(user=instance)
