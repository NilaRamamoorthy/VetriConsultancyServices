from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import CandidateProfile
from .models import Course, Enrollment
from django.contrib import messages

@login_required
def course_list_view(request):
    courses = Course.objects.all()
    candidate = request.user.profile  # CandidateProfile
    enrolled_course_ids = candidate.enrollments.values_list('course_id', flat=True)
    return render(request, 'training/course_list.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids,
    })



@login_required
def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    candidate = request.user.profile
    subscription = getattr(request.user, 'subscription', None)  # safe access

    # Check if already enrolled
    enrollment = Enrollment.objects.filter(candidate=candidate, course=course).first()

    if request.method == 'POST':
        if subscription and subscription.is_pro():
            if not enrollment:
                enrollment = Enrollment.objects.create(candidate=candidate, course=course)
                messages.success(request, f"You are now enrolled in {course.title}!")
            return redirect('training:my_courses')
        else:
            messages.warning(request, "You need a Pro subscription to enroll in this course.")
            return redirect('subscriptions:plans')

    return render(request, 'training/course_detail.html', {
        'course': course,
        'enrollment': enrollment,
        'subscription': subscription,
    })


@login_required
def enroll_course_view(request, course_id):
    if not request.user.subscription.is_pro():
        messages.warning(request, "You need a Pro subscription to enroll in courses.")
        return redirect('subscriptions:plans')

    candidate = request.user.profile
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(candidate=candidate, course=course)
    if created:
        messages.success(request, f"Successfully enrolled in {course.title}")
    return redirect('training:my_courses')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import CandidateProfile
from .models import Course, Enrollment

@login_required
def my_courses_view(request):
    candidate = request.user.profile  # CandidateProfile
    enrollments = Enrollment.objects.filter(candidate=candidate).select_related('course')
    return render(request, "training/my_courses.html", {
        "enrollments": enrollments
    })

@login_required
def my_course_detail_view(request, course_id):
    candidate = request.user.profile
    enrollment = get_object_or_404(Enrollment, candidate=candidate, course_id=course_id)

    return render(request, "training/my_course_detail.html", {
        "enrollment": enrollment
    })

