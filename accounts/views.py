from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.mail import send_mail
from django.utils.html import strip_tags

from accounts.models import User
from profiles.models import CandidateProfile

# ----------------------------
# Home View
# ----------------------------
def home_view(request):
    return render(request, 'accounts/home.html')


# ----------------------------
# Signup Form
# ----------------------------
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password2', "Passwords do not match")
        return cleaned_data


# ----------------------------
# Signup View
# ----------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Send welcome email
            subject = "Welcome to Vetri Consultancy!"
            role_text = "Employer" if user.role == 'EMPLOYER' else "Candidate"
            html_message = f"""
            <html><body>
            <h2>Welcome, {role_text}!</h2>
            <p>Hi {user.email}, welcome to <strong>Vetri Consultancy</strong>!</p>
            <p><a href="http://127.0.0.1:8000/accounts/login/">Login Now</a></p>
            </body></html>
            """
            send_mail(
                subject,
                strip_tags(html_message),
                None,  # DEFAULT_FROM_EMAIL
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            login(request, user)
            return redirect('jobs:jobs_list')  # ✅ after signup, go to jobs list
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


# ----------------------------
# Login Form
# ----------------------------
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


# ----------------------------
# Login View
# ----------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('jobs:jobs_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('jobs:jobs_list')  # ✅ after login, go to jobs
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'hide_nav': True
    })


# ----------------------------
# Dashboard View
# ----------------------------
# @login_required
# def dashboard_view(request):
#     user = request.user
#     profile, _ = CandidateProfile.objects.get_or_create(user=user)
#     profile_completion = profile.profile_completeness()

#     template = (
#         'accounts/dashboard_candidate.html' if user.role == "CANDIDATE" else
#         'accounts/dashboard_consultant.html' if user.role == "CONSULTANT" else
#         'accounts/dashboard_admin.html'
#     )

#     return render(request, template, {
#         'user': user,
#         'profile_completion': profile_completion,
#         'profile': profile,
#     })

from subscriptions.models import Subscription
from profiles.models import CandidateProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard_view(request):
    user = request.user
    profile_completion = None
    profile = None
    subscription = None

    if user.role == "CANDIDATE":
        profile, _ = CandidateProfile.objects.get_or_create(user=user)
        profile_completion = profile.profile_completeness()

        # get or create subscription (safe)
        subscription, _ = Subscription.objects.get_or_create(user=user)

    template = (
        'accounts/dashboard_candidate.html' if user.role == "CANDIDATE" else
        'accounts/dashboard_consultant.html' if user.role == "CONSULTANT" else
        'accounts/dashboard_admin.html'
    )

    return render(request, template, {
        'user': user,
        'profile': profile,
        'profile_completion': profile_completion,
        'subscription': subscription,  # 👈 NEW
    })


# ----------------------------
# Candidate Profile Form & View
# ----------------------------
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        # Replace full_name with first_name and last_name
        fields = [
            'first_name', 'last_name', 'phone', 'location',
            'experience_years', 'skills', 'resume', 'profile_image'
        ]
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django'}),
        }


@login_required
def candidate_profile_view(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:dashboard')  # ✅ redirect using namespace
    else:
        form = CandidateProfileForm(instance=profile)

    profile_completion = profile.profile_completeness()

    return render(request, 'profiles/candidate_profile.html', {
        'form': form,
        'profile_completion': profile_completion
    })


from django.db.models import Q

from jobs.models import JobQuery

@login_required
def consultant_dashboard_view(request):
    user = request.user

    unread_queries_count = JobQuery.objects.filter(
        job__posted_by=user,
        is_resolved=False
    ).count()

    return render(request, 'accounts/dashboard_consultant.html', {
        'unread_queries_count': unread_queries_count
    })
