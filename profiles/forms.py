from django import forms
from .models import ConsultantProfile

class ConsultantProfileForm(forms.ModelForm):
    class Meta:
        model = ConsultantProfile
        fields = [
            'first_name',
            'last_name',
            'phone',
            'company',
            'designation',
            'profile_image',
            'bio',
            'linkedin',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something about yourself...'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'LinkedIn profile URL'}),
        }
