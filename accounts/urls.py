from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'  # ✅ namespace required for {% url 'accounts:...' %}

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.candidate_profile_view, name='candidate_profile'),
]
