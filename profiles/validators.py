from django.core.exceptions import ValidationError

def validate_file_size_5mb(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("Resume file size must be under 5MB.")
