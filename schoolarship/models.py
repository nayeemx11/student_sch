from django.db import models
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    student_identity_number = models.CharField(max_length=10, null=True, blank=True)
    current_status = models.CharField(
        max_length=20,
        choices=[
            ("Freshman", "Freshman"),
            ("Sophomore", "Sophomore"),
            ("Junior", "Junior"),
            ("Senior", "Senior"),
        ],
    )
    cumulative_gpa = models.FloatField(null=True)
    credit_hours = models.IntegerField(null=True)
    eligible_for_application = models.BooleanField(default=False)
    gpa_this_semester = models.FloatField(null=True)


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_applied = models.DateField(auto_now_add=True)
    scholarship_status = models.BooleanField(default=False)
    applied = models.BooleanField(default=False)
    can_get_scholarship = models.BooleanField(default=False)


class Award(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    awarded_date = models.DateField(auto_now_add=True)
    bill_amount = models.FloatField()
    balance = models.FloatField()
    gets_scholarship = models.BooleanField()
