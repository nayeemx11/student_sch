from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student, Application, Award
from .forms import StudentUpdateForm


# student must be update his information before applying
@login_required
def update_student_info(request):
    # Fetch the logged-in user's student profile
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()  # Save the updated student info
            messages.success(request, "Your information has been updated successfully!")
            return redirect("index")  # Redirect to the index or another page
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, "update_student_info.html", {"form": form})


# verify student he/she can be able to apply for scholarship
@login_required
def verify_student(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        student_form = StudentUpdateForm(request.POST, instance=student)

        if student_form.is_valid():
            cleaned_data_student_form = student_form.cleaned_data
            # get matched with the registration office info
            if (
                cleaned_data_student_form["current_status"] == student.current_status
                and cleaned_data_student_form["cumulative_gpa"]
                == student.cumulative_gpa
                and cleaned_data_student_form["credit_hours"] == student.credit_hours
            ):
                student.eligible_for_application = True
                student.save()
                messages.success(
                    request,
                    "Verification successful! Student is now eligible to apply for a scholarship.",
                )
            else:
                messages.error(
                    request,
                    "Verification failed. Please ensure all student data is correct.",
                )
            return redirect("verify_student")
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, "apply.html", {"form": form, "student": student})



# student can apply for scholarship and create application
@login_required
def apply_scholarship(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST" and student.eligible_for_application == True:
        # Create an application instance for the student
        Application.objects.create(
            student=student,
            applied=True,
        )
        messages.success(request, "Application submitted successfully!")
        return redirect("index")
    else:
        messages.error(request, "Data mismatch with Register.")

        # two times applied
        # if applicant is eligible

    return render(request, "index.html")



# checks criteria  
def check_eligibility(request):
    applications = Application.objects.filter(applied=True)
    current_year = timezone.now().year
    # Eligibility criteria
    for application in applications:
        student = application.student
        age_at_application = current_year - student.user.date_of_birth.year
        if (
            student.cumulative_gpa >= 3.2
            and student.credit_hours >= 12
            and age_at_application <= 23
        ):
            application.can_get_scholarship = True
        else:
            application.can_get_scholarship = False
        application.save()



@login_required
def committee_dashboard(request):
    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).order_by("-student__cumulative_gpa")

    if eligible_applications.exists():
        # Only access the first application if there are eligible applications
        student_gets_scholarship = eligible_applications[0].student
    else:
        student_gets_scholarship = None  # No eligible student

    return render(
        request,
        "committee_dashboard.html",
        {
            "student_eligible": eligible_applications,
            "student_gets_scholarship": student_gets_scholarship,
        },
    )




@login_required
def award_scholarship(request):
    check_eligibility(request)
    # Ensure eligibility is checked before filtering eligible applications

    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).order_by("-student__cumulative_gpa")

    if not eligible_applications.exists():
        messages.error(request, "No eligible applicants found.")
        return redirect("committee_dashboard")  # Redirect if no eligible applicants

    # Find the top GPA students
    top_gpa = eligible_applications[0].student.cumulative_gpa
    top_students = [
        app for app in eligible_applications if app.student.cumulative_gpa == top_gpa
    ]

    # Apply tie-breaking rules if necessary
    if len(top_students) > 1:
        top_students.sort(
            key=lambda x: (
                -x.student.gpa_this_semester,  # Prefer higher semester GPA
                x.student.current_status == "Junior",  # Prefer Juniors
                x.student.user_gender == "Female",  # Prefer females
                x.student.date_of_birth,  # Prefer older students
            )
        )

    # Select the winner
    winner = top_students[0].student

    # Create an award for the winner
    Award.objects.create(
        student=winner,
        bill_amount=5000,
        balance=1500,
        gets_scholarship=True,
    )

    # Now, return the rendered template with the necessary context
    return render(
        request,
        "committee_dashboard.html",
        {
            "student_eligible": eligible_applications,
            "student_gets_scholarship": winner,
        },
    )



@login_required
def send_mail_to_awarded_student(request):
    try:
        winner = Award.objects.get(gets_scholarship=True)
    except Award.DoesNotExist:
        messages.error(request, "No awarded student found.")
        return redirect("committee_dashboard")

    # # Send congratulatory email to winner
    # send_mail(
    #     "Congratulations!",
    #     f"Dear {winner.student.user.first_name}, you have been awarded the Smart Scholarship.",
    #     "admin@example.com",
    #     [winner.student.user.email],
    # )

    messages.success(
        request,
        f"Scholarship awarded to {winner.student.user.first_name} {winner.student.user.last_name}.",
    )

    return redirect("committee_dashboard")


@login_required
def notify_other_eligible_applicants(request):
    try:
        winner = Award.objects.get(gets_scholarship=True)
    except Award.DoesNotExist:
        messages.error(request, "No awarded student found.")
        return redirect("committee_dashboard")

    # Notify other eligible applicants
    eligible_applications = Application.objects.filter(
        can_get_scholarship=True
    ).exclude(student=winner.student)

    # for application in eligible_applications:
    #     send_mail(
    #         "Scholarship Outcome",
    #         f"Dear {application.student.user.first_name}, unfortunately you were not selected for the scholarship.",
    #         "admin@example.com",
    #         [application.student.user.email],
    #     )

    return redirect("committee_dashboard")
