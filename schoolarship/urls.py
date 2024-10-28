from django.urls import path
from . import views

urlpatterns = [
    path('update_student_info/', views.update_student_info, name='update_student_info'),
    
    # is matching with reg
    path('verify_student/', views.verify_student, name='verify_student'),
    
    # this is for application
    path('apply_scholarship/', views.apply_scholarship, name='apply_scholarship'),
    
    path('award_scholarship', views.award_scholarship, name='award_scholarship'),
    path('send_mail_to_awarded_student/', views.send_mail_to_awarded_student, name='send_mail_to_awarded_student'),
    path('notify-other-eligible/', views.notify_other_eligible_applicants, name='notify_other_eligible_applicants'),
    path('committee_dashboard/', views.committee_dashboard, name='committee_dashboard'),
]