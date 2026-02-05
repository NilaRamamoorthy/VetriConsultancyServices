from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CandidateProfile

@login_required
def candidate_profile_view(request):
    profile, _ = CandidateProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.first_name = request.POST.get("first_name", "")
        profile.last_name = request.POST.get("last_name", "")
        profile.phone = request.POST.get("phone", "")
        profile.location = request.POST.get("location", "")
        profile.skills = request.POST.get("skills", "")
        profile.experience_years = request.POST.get("experience_years") or None

        # ✅ HANDLE PROFILE IMAGE
        if "profile_image" in request.FILES:
            if profile.profile_image:
                profile.profile_image.delete(save=False)
            profile.profile_image = request.FILES["profile_image"]
            


        # ✅ HANDLE RESUME
        if "resume" in request.FILES:
            if profile.resume:
                profile.resume.delete(save=False)
            profile.resume = request.FILES["resume"]
        profile.full_clean()
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profiles:candidate_profile")

    skills_list = (
        [s.strip() for s in profile.skills.split(",") if s.strip()]
        if profile.skills else []
    )

    return render(request, "profiles/candidate_profile.html", {
        "profile": profile,
        "skills_list": skills_list
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultantProfileForm
from .models import ConsultantProfile

@login_required
def consultant_profile_view(request):
    """
    Show and edit the consultant profile.
    Auto-creates profile if missing.
    """
    # Auto-create if missing
    profile, created = ConsultantProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ConsultantProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultant profile updated successfully.")
            return redirect('accounts:dashboard')
    else:
        form = ConsultantProfileForm(instance=profile)

    profile_completion = profile.profile_completeness()

    return render(request, 'profiles/consultant_profile.html', {
        'form': form,
        'profile_completion': profile_completion
    })

