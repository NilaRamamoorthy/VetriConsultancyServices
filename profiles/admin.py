from django.contrib import admin
from .models import CandidateProfile

class CandidateProfileAdmin(admin.ModelAdmin):
    # Replace 'full_name' with 'first_name' and 'last_name' or create a callable
    list_display = ('user', 'first_name', 'last_name', 'phone', 'location', 'experience_years')

    # Optional: if you want a single column showing full name
    # def full_name(self, obj):
    #     return f"{obj.first_name} {obj.last_name}"
    # full_name.short_description = 'Full Name'
    # list_display = ('user', 'full_name', 'phone', 'location', 'experience_years')

admin.site.register(CandidateProfile, CandidateProfileAdmin)
