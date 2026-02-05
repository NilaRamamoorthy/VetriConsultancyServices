from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'company',
            'location',
            'experience',
            'job_type',
            'domain',
            'skills',
            'description',
            'is_active'
        ]


from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your cover letter (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        candidate_profile = kwargs.pop('candidate_profile', None)
        super().__init__(*args, **kwargs)
        if candidate_profile and candidate_profile.resume:
            self.fields['resume'].initial = candidate_profile.resume


# jobs/forms.py
from django import forms
from .models import JobQuery, JobQueryReply

class JobQueryForm(forms.ModelForm):
    class Meta:
        model = JobQuery
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ask your question...'})
        }

class JobQueryReplyForm(forms.ModelForm):
    class Meta:
        model = JobQueryReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Type your reply...'})
        }
