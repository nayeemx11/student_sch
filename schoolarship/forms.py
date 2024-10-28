from django import forms
from .models import Application, Student

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_identity_number",
            "current_status",
            "cumulative_gpa",
            "credit_hours",
            "eligible_for_application",
        ]


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_identity_number",
            "current_status",
            "cumulative_gpa",
            "credit_hours",
            "gpa_this_semester",
        ]
