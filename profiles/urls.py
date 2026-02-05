from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("candidate/", views.candidate_profile_view, name="candidate_profile"),
    path('dashboard/consultant-profile/', views.consultant_profile_view, name='consultant_profile'),

]
