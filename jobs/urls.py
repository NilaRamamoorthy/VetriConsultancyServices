from django.urls import path
from .views import (
    jobs_list_view,
    job_detail_view,
    save_job_view,
    unsave_job_view,
    apply_job_view,
    saved_jobs_list_view,
    post_job_view,
    posted_jobs_view,
    edit_job_view,
    delete_posted_job_view,
    applicants_list_view,
    applicant_detail_view,
    shortlisted_applicants_view,
    candidate_applied_jobs_view,
    job_queries_view,
    recommended_jobs_view,
    query_queue_view,  # ✅ Consultant Query Queue
    resolve_query_view     
)

app_name = "jobs"

urlpatterns = [

    # ============================
    # STATIC / LIST PAGES
    # ============================
    path('', jobs_list_view, name='jobs_list'),
    path('saved/', saved_jobs_list_view, name='saved_jobs'),
    path('post/', post_job_view, name='post_job'),
    path('posted/', posted_jobs_view, name='posted_jobs'),

    # ============================
    # JOB ACTIONS
    # ============================
    path('<int:job_id>/save/', save_job_view, name='save_job'),
    path('<int:job_id>/unsave/', unsave_job_view, name='unsave_job'),
    path('<int:job_id>/apply/', apply_job_view, name='apply_job'),
    path('<int:job_id>/edit/', edit_job_view, name='edit_job'),
    path('<int:job_id>/delete/', delete_posted_job_view, name='delete_job'),

    # ============================
    # JOB DETAILS
    # ============================
    path('<int:job_id>/', job_detail_view, name='job_detail'),

    # ============================
    # APPLICANTS
    # ============================
    path('<int:job_id>/applicants/', applicants_list_view, name='applicants_list'),
    path('applicant/<int:application_id>/', applicant_detail_view, name='applicant_detail'),
    path('shortlisted/', shortlisted_applicants_view, name='shortlisted_applicants'),
    path('my-applications/', candidate_applied_jobs_view, name='candidate_applied_jobs'),

    # ============================
    # JOB QUERIES / CHAT
    # ============================
    path('<int:job_id>/queries/', job_queries_view, name='job_queries'),
    path('queries/queue/', query_queue_view, name='query_queue'),  # Consultant queue
    path('queries/<int:query_id>/resolve/', resolve_query_view, name='resolve_query'),

    # ============================
    # RECOMMENDED JOBS
    # ============================
    path('recommended/', recommended_jobs_view, name='recommended_jobs'),
]
