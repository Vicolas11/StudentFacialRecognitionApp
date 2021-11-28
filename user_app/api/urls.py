from django.urls import path, re_path
from django.views.generic.base import TemplateView
from user_app.api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),   
    path('login/lecturer/', views.LecturerLoginView.as_view(), name='login_lecturer'),
    path('login/student/', views.StudentLoginView.as_view(), name='login_student'),
    path('register/lecturer/', views.LecturerRegistrationView.as_view(), name='register_lecturer'),
    path('register/student/', views.StudentRegistrationView.as_view(), name='register_student'),  
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('lecturer_update_profile/', views.LecturerProfileUpdateView.as_view(), name='lecturer_update_profile'),
    path('student_update_profile/', views.StudentProfileUpdateView.as_view(), name='student_update_profile'),
    path('upload_avatar/', views.UserAvatarUpload.as_view(), name='upload_avatar'), 
    path('users-list/', views.UsersListView.as_view(), name='users_list'),
    # Account Activation
    path('activation_sent/', TemplateView.as_view(template_name='activate_sent.html'), name='activate_sent'),
    path('activate/<slug:uidb64>/<slug:token>', views.activate_account, name='activate'),
    path('activated_completed/', TemplateView.as_view(template_name='activated_completed.html'), name='activated_completed'),
    path('activated_failed/', TemplateView.as_view(template_name='activation_invalid.html'), name='activation_invalid'),
]