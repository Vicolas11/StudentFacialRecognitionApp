from facial_app.models import Attendance, CreateAttendance, Student, User
from django.contrib import messages
from django.shortcuts import redirect, render
from user_app.mixin import LecturerLoginRequiredMixin, StudentLoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView


class DashBoardView(LecturerLoginRequiredMixin, TemplateView):
	template_name = 'create_attendance.html'


class LecturerProfileView(LecturerLoginRequiredMixin, TemplateView):
	template_name = 'profile_lecturer.html' 

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			"CreatedAttendance": CreateAttendance.objects.filter(user=self.request.user).order_by('-id')
		})
		return context


class LecturerProfileEditView(LecturerLoginRequiredMixin, TemplateView):
	template_name = 'profile_lecturer_edit.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			"Departments": ['Computer Science','Mathematics','Statistics','Physics','Chemistry','Biology','Political Science','Economics','Mass Communication','History','English'],
			"Faculties": ['Science','Social Science','Arts'],
			"Gender": ['Male','Female']
		})
		return context


class StudentProfileView(StudentLoginRequiredMixin, TemplateView):
	template_name = 'profile_student.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		totalAttendance = CreateAttendance.objects.filter(
			level=self.request.user.student.level, 
			department=self.request.user.student.department).count()
		attended = Attendance.objects.filter(
			student=self.request.user, 
			level=self.request.user.student.level,
			matric_no=self.request.user.student.matric_no, 
			department=self.request.user.student.department, 
			present = "Present").count()
		AvgAttendance = None
		if AvgAttendance:
			AvgAttendance = (attended/totalAttendance) * 100
		context.update({
			"StudentAttendance": Attendance.objects.filter(student=self.request.user, matric_no=self.request.user.student.matric_no).order_by('-id'),
			"TotalAttendance": attended
		})
		return context


class StudentProfileEditView(StudentLoginRequiredMixin, TemplateView):
	template_name = 'profile_student_edit.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		Years = self.request.user.student.dob.year
		Months = self.request.user.student.dob.month
		Days = self.request.user.student.dob.day	
		context.update({
			"Departments": ['Computer Science','Mathematics','Statistics','Physics','Chemistry','Biology','Political Science','Economics','Mass Communication','History','English'],
			"Levels": ['100','200','300','400'],
			"Gender": ['Male','Female'],
			"Semesters": ['First','Second'],
			"Year": f'{Years}',
			"Month": f'0{Months}' if Months < 10 else f'{Months}',
			"Day": f'0{Days}' if Days < 10 else f'{Days}',
		})
		return context


class TakeAttendanceCreateView(StudentLoginRequiredMixin, TemplateView):
	template_name = 'take_attendance.html'


class AttendanceListView(LecturerLoginRequiredMixin, TemplateView):
	template_name = 'view_attendance.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update({
			"GeneralAttendance": Attendance.objects.filter(lecturer=self.request.user)
		})
		return context


class FeedbackCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'feedback.html'


class PasswordRestConfirm(TemplateView):
	template_name = 'passwordreset/password_reset_confirm.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.session['reset_link'] is not None:
			get_cookies = self.request.session['reset_link']
			data.update({
				'token': get_cookies
			})
			return data