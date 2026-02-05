from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course_view, name='enroll_course'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path("my-courses/<int:course_id>/", views.my_course_detail_view, name="my_course_detail"),
]
