from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Job, SavedJob, Application
from profiles.models import CandidateProfile
from .forms import JobForm


# ============================
# JOB LIST
# ============================
@login_required
def jobs_list_view(request):
    user = request.user

    # All active jobs
    jobs = Job.objects.filter(is_active=True).order_by('-posted_on')

    # If consultant, show only their own jobs
    if user.role == 'CONSULTANT':
        jobs = jobs.filter(posted_by=user)

    # --------------------
    # Filters (for candidates)
    # --------------------
    if user.role == 'CANDIDATE':
        experience = request.GET.get('experience')
        location = request.GET.get('location')
        job_type = request.GET.get('job_type')
        domain = request.GET.get('domain')
        skills = request.GET.get('skills')

        if experience:
            jobs = jobs.filter(experience__lte=experience)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if domain:
            jobs = jobs.filter(domain__icontains=domain)
        if skills:
            jobs = jobs.filter(skills__icontains=skills)

    # --------------------
    # Saved & Applied jobs (⭐ only for candidates)
    # --------------------
    saved_job_ids = set()
    applied_job_ids = set()
    if user.role == 'CANDIDATE':
        saved_job_ids = set(SavedJob.objects.filter(user=user).values_list('job_id', flat=True))
        applied_job_ids = set(Application.objects.filter(user=user).values_list('job_id', flat=True))

    # --------------------
    # Pagination
    # --------------------
    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/jobs_list.html', {
        'page_obj': page_obj,
        'filters': request.GET,
        'saved_job_ids': saved_job_ids,
        'applied_job_ids': applied_job_ids,
    })


# ============================
# JOB DETAIL
# ============================
@login_required
def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    applied = False
    saved = False
    is_owner = False
    application = None  # Will hold candidate's application if exists

    # Candidate view
    if user.role == 'CANDIDATE':
        try:
            application = Application.objects.get(user=user, job=job)
            applied = True
        except Application.DoesNotExist:
            applied = False

        saved = SavedJob.objects.filter(user=user, job=job).exists()

    # Consultant owner view
    if user.role == 'CONSULTANT' and job.posted_by == user:
        is_owner = True

    applicants_count = job.applications.count()  # Total applicants for this job

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'applied': applied,
        'saved': saved,
        'is_owner': is_owner,
        'applicants_count': applicants_count,
        'application': application,  # Pass the actual application object
    })


# ============================
# SAVE / UNSAVE JOB
# ============================
@login_required
def save_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )

    messages.success(request, "Job saved successfully.")
    return redirect('jobs:job_detail', job_id=job.id)


@login_required
def unsave_job_view(request, job_id):
    SavedJob.objects.filter(
        user=request.user,
        job_id=job_id
    ).delete()

    return redirect('jobs:saved_jobs')


# ============================
# APPLY JOB
# ============================
# jobs/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application
from profiles.models import CandidateProfile
from .forms import ApplicationForm

@login_required
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    if user.role != 'CANDIDATE':
        return redirect('jobs:jobs_list')

    # Get candidate profile
    profile = CandidateProfile.objects.get(user=user)

    # Prevent duplicate applications
    if Application.objects.filter(user=user, job=job).exists():
        return redirect('jobs:job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, candidate_profile=profile)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.job = job

            # Use profile resume if no new resume uploaded
            if not application.resume:
                application.resume = profile.resume

            application.save()
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = ApplicationForm(candidate_profile=profile)

    return render(request, 'jobs/apply_job.html', {
        'job': job,
        'profile': profile,
        'form': form
    })


# ============================
# SAVED JOBS LIST
# ============================
@login_required
def saved_jobs_list_view(request):
    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job')

    return render(request, 'jobs/saved_jobs.html', {
        'saved_jobs': saved_jobs
    })


# ============================
# POST JOB (CONSULTANT)
# ============================
@login_required
def post_job_view(request):
    if request.user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    if request.method == 'POST':
        Job.objects.create(
            posted_by=request.user,
            title=request.POST.get('title'),
            company=request.POST.get('company'),
            location=request.POST.get('location'),
            experience=request.POST.get('experience'),
            job_type=request.POST.get('job_type'),
            domain=request.POST.get('domain'),
            skills=request.POST.get('skills'),
            description=request.POST.get('description'),
        )
        return redirect('jobs:posted_jobs')

    return render(request, 'jobs/post_job.html')


# ============================
# POSTED JOBS LIST (CONSULTANT)
# ============================
@login_required
def posted_jobs_view(request):
    if request.user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    jobs = Job.objects.filter(
        posted_by=request.user
    ).order_by('-posted_on')

    return render(request, 'jobs/posted_jobs.html', {
        'jobs': jobs
    })


# ============================
# EDIT POSTED JOB
# ============================
@login_required
def edit_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'CONSULTANT' or job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this job.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs:job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {
        'form': form,
        'job': job
    })


# ============================
# DELETE POSTED JOB
# ============================
@login_required
def delete_posted_job_view(request, job_id):
    if request.user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    job = get_object_or_404(
        Job,
        id=job_id,
        posted_by=request.user
    )

    job.delete()  # applications + saved jobs auto-delete
    return redirect('jobs:posted_jobs')

# ============================
#  Applicants List
# ============================

@login_required
def applicants_list_view(request, job_id):
    # Get the job
    job = get_object_or_404(Job, id=job_id)

    # Only the consultant who posted this job can view applicants
    if request.user.role != 'CONSULTANT' or job.posted_by != request.user:
        return HttpResponseForbidden("You are not allowed to view applicants for this job.")

    # Get all applications for this job, order by applied_at descending
    applications = Application.objects.filter(job=job).select_related('user', 'job').order_by('-applied_at')

    return render(request, 'jobs/applicants_list.html', {
        'job': job,
        'applications': applications
    })

# ============================
#  Applicants Detail
# ============================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Application

@login_required
def applicant_detail_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'CONSULTANT' or application.job.posted_by != request.user:
        return redirect('jobs:jobs_list')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'shortlist':
            application.status = 'SHORTLISTED'
            application.save()

        elif action == 'reject':
            application.status = 'REJECTED'
            application.save()

        elif action == 'schedule_meeting':
            dt = request.POST.get('meeting_datetime')
            if dt:
                application.meeting_datetime = dt
                application.meeting_status = 'SCHEDULED'
                application.save()

        elif action == 'change_meeting':
            dt = request.POST.get('meeting_datetime')
            if dt:
                application.meeting_datetime = dt
                application.meeting_status = 'SCHEDULED'
                application.save()

        elif action == 'cancel_meeting':
            application.meeting_datetime = None
            application.meeting_status = 'NOT_SCHEDULED'
            application.save()

        return redirect('jobs:applicant_detail', application_id=application.id)

    return render(request, 'jobs/applicant_detail.html', {
        'application': application
    })


# ============================
#  Shortlisted Applicants
# ============================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Application, Job

@login_required
def shortlisted_applicants_view(request):
    if request.user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    # Get all applications where the consultant owns the job AND status is SHORTLISTED
    applications = Application.objects.filter(
        job__posted_by=request.user,
        status='SHORTLISTED'
    ).order_by('-applied_at')

    return render(request, 'jobs/shortlisted_applicants.html', {
        'applications': applications
    })

# ============================
#  Candidate Applications
# ============================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Application

@login_required
def candidate_applied_jobs_view(request):
    user = request.user

    # Get all applications of this candidate
    applications = Application.objects.filter(user=user).order_by('-applied_at')

    return render(request, 'jobs/candidate_applied_jobs.html', {
        'applications': applications
    })


# ============================
#  Job Queries
# ============================

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Job, JobQuery, JobQueryReply

@login_required
def job_queries_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    # -----------------------------
    # Permission check
    # -----------------------------
    if user.role == 'CANDIDATE':
        queries = JobQuery.objects.filter(job=job, user=user).order_by('created_at')
    elif user.role == 'CONSULTANT' and job.posted_by == user:
        queries = JobQuery.objects.filter(job=job).order_by('created_at')
    else:
        return redirect('jobs:jobs_list')

    # -----------------------------
    # Candidate submits new query
    # -----------------------------
    if request.method == 'POST' and user.role == 'CANDIDATE':
        question = request.POST.get('question')
        if question:
            JobQuery.objects.create(job=job, user=user, question=question)
            return redirect('jobs:job_queries', job_id=job.id)

    # -----------------------------
    # Consultant replies to a query
    # -----------------------------
    if request.method == 'POST' and user.role == 'CONSULTANT':
        query_id = request.POST.get('query_id')
        message = request.POST.get('message')
        if query_id and message:
            query = get_object_or_404(JobQuery, id=query_id, job=job)
            JobQueryReply.objects.create(query=query, user=user, message=message)
            return redirect('jobs:job_queries', job_id=job.id)

    return render(request, 'jobs/job_queries.html', {
        'job': job,
        'queries': queries,
        'user': user
    })

# -----------------------------
# Recomended Jobs
# -----------------------------
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from profiles.models import CandidateProfile
from .models import Job, Application, SavedJob


@login_required
def recommended_jobs_view(request):
    user = request.user

    if user.role != 'CANDIDATE':
        return redirect('jobs:jobs_list')

    profile = getattr(user, 'profile', None)

    if not profile or not profile.skills:
        jobs = Job.objects.none()
    else:
        skills = [s.strip().lower() for s in profile.skills.split(',') if s.strip()]

        query = Q()
        for skill in skills:
            query |= (
                Q(title__icontains=skill) |
                Q(domain__icontains=skill) |
                Q(description__icontains=skill)
            )

        jobs = Job.objects.filter(query).distinct().order_by('-posted_on')

    # Applied & Saved jobs
    applied_job_ids = Application.objects.filter(
        user=user
    ).values_list('job_id', flat=True)

    saved_job_ids = SavedJob.objects.filter(
        user=user
    ).values_list('job_id', flat=True)

    paginator = Paginator(jobs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/recommended_jobs.html', {
        'page_obj': page_obj,
        'applied_job_ids': applied_job_ids,
        'saved_job_ids': saved_job_ids,
    })

# -----------------------------
# Consultant Query Queue
# -----------------------------

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import JobQuery, Job

@login_required
def consultant_query_queue_view(request):
    user = request.user

    if user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    # All queries for jobs posted by this consultant
    queries = JobQuery.objects.filter(
        job__posted_by=user
    ).select_related('job', 'user').order_by('-created_at')

    return render(request, 'jobs/consultant_query_queue.html', {
        'queries': queries
    })

@login_required
def resolve_query_view(request, query_id):
    query = get_object_or_404(JobQuery, id=query_id)

    # Only consultant who owns the job
    if request.user.role != 'CONSULTANT' or query.job.posted_by != request.user:
        return redirect('jobs:jobs_list')

    query.is_resolved = not query.is_resolved
    query.save()

    return redirect('jobs:job_queries', job_id=query.job.id)



@login_required
def query_queue_view(request):
    user = request.user

    if user.role != 'CONSULTANT':
        return redirect('jobs:jobs_list')

    queries = (
        JobQuery.objects
        .filter(job__posted_by=user)
        .select_related('job', 'user')
        .order_by('is_resolved', '-created_at')
    )

    return render(request, 'jobs/query_queue.html', {
        'queries': queries
    })



@login_required
def job_queries_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    if user.role == 'CANDIDATE':
        queries = JobQuery.objects.filter(job=job, user=user)
    elif user.role == 'CONSULTANT' and job.posted_by == user:
        queries = JobQuery.objects.filter(job=job)
    else:
        return redirect('jobs:jobs_list')

    # Send message
    if request.method == 'POST':
        if 'message' in request.POST:
            query_id = request.POST.get('query_id')
            message = request.POST.get('message')

            query = get_object_or_404(JobQuery, id=query_id)
            JobQueryReply.objects.create(
                query=query,
                user=user,
                message=message
            )

            return redirect('jobs:job_queries', job_id=job.id)

        # Mark resolved
        if 'resolve' in request.POST and user.role == 'CONSULTANT':
            query_id = request.POST.get('query_id')
            JobQuery.objects.filter(id=query_id).update(is_resolved=True)
            return redirect('jobs:job_queries', job_id=job.id)

    return render(request, 'jobs/job_queries.html', {
        'job': job,
        'queries': queries
    })
