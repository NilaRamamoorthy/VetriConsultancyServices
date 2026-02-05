# training/admin.py
from django.contrib import admin
from .models import Course, Enrollment

# ----------------------------
# Course Admin
# ----------------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

# ----------------------------
# Enrollment Admin
# ----------------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'course', 'progress', 'completed', 'applied_at')
    list_filter = ('completed', 'course')
    search_fields = ('candidate__user__email', 'course__title')
    ordering = ('-applied_at',)

    # Optional: allow admin to edit these fields directly from the list view
    list_editable = ('progress', 'completed')
