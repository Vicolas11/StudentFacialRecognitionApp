from django.urls import path
from django.conf import settings
from facial_app import views
from django.views.generic import TemplateView
from django.conf.urls.static import static

app_name = 'facial'
urlpatterns = [
    path('', TemplateView.as_view(template_name='landingPage.html'), name='home'),
    path('login/admin/', TemplateView.as_view(template_name='login_admin.html'), name='login_admin'),
    path('login/student/', TemplateView.as_view(template_name='login_student.html'), name='login_student'),
    path('login/lecturer/', TemplateView.as_view(template_name='login_lecturer.html'), name='login_lecturer'),
    path('signup/student/', TemplateView.as_view(template_name='signup_student.html'), name='signup_student'),
    path('signup/lecturer/', TemplateView.as_view(template_name='signup_lecturer.html'), name='signup_lecturer'),
    path('password_reset/', TemplateView.as_view(template_name='passwordreset/password_reset_form.html'), name='password_reset'),
    path('password_confirm/', views.PasswordRestConfirm.as_view(), name='password_confirm'),
    path('create/attendance/', views.DashBoardView.as_view(), name='create_attendance'),
    path('attendance/', views.AttendanceListView.as_view(), name='view_attendance'),
    path('take/attendance/', views.TakeAttendanceCreateView.as_view(), name='take_attendance'),
    path('profile/student/', views.StudentProfileView.as_view(), name='profile_student'),
    path('profile/lecturer/', views.LecturerProfileView.as_view(), name='profile_lecturer'),
    path('feedback/', views.FeedbackCreateView.as_view(), name='feedback'),
    path('profile/student/edit/', views.StudentProfileEditView.as_view(), name='profile_student_edit'),
    path('profile/lecturer/edit/', views.LecturerProfileEditView.as_view(), name='profile_lecturer_edit'),
]