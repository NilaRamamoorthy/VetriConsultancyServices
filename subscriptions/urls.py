# subscriptions/urls.py
from django.urls import path
from . import views

app_name = 'subscriptions'   # 🔴 THIS IS REQUIRED

urlpatterns = [
    path('plans/', views.subscription_plans_view, name='plans'),
    path('subscribe/pro/', views.subscribe_pro_view, name='subscribe_pro'),
    path('payment/', views.dummy_payment_view, name='payment'),
]
