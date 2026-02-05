from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'experience', 'location', 'is_active')
    list_filter = ('job_type', 'experience', 'location', 'domain', 'is_active')
    search_fields = ('title', 'company', 'skills', 'domain')
