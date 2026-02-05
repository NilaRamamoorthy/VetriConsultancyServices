# subscriptions/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Subscription


@login_required
def subscription_plans_view(request):
    """
    Show Free & Pro plans
    """
    subscription, _ = Subscription.objects.get_or_create(user=request.user)

    return render(request, 'subscriptions/plans.html', {
        'subscription': subscription
    })


@login_required
def subscribe_pro_view(request):
    """
    Handle Pro subscription (dummy – redirects to payment)
    """
    subscription, _ = Subscription.objects.get_or_create(user=request.user)

    # Already Pro → no need to pay again
    if subscription.is_pro:
        return redirect('accounts:dashboard')

    return redirect('subscriptions:payment')


@login_required
def dummy_payment_view(request):
    """
    Fake payment page → upgrades to Pro
    """
    subscription, _ = Subscription.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        subscription.plan = 'PRO'
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=30)
        subscription.save()
        print("REQUEST METHOD:", request.method)

        return redirect('accounts:dashboard')

    return render(request, 'subscriptions/payment.html')
