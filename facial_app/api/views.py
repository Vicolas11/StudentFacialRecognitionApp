from facial_app.timeout import TimeoutVar
from facial_app.recognizer import Recognizer
from facial_app.random_num import id_generator
from rest_framework.response import Response
from rest_framework.views import APIView
from facial_app.api.serializers import (AttendanceSerializer, CreateAttendanceSerializer, FeedbackSerializer, TakeAttendanceSerializer)
from facial_app.models import Attendance, CreateAttendance, Feedback, Lecturer, Student
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, serializers, status
from django.contrib import messages
from django.core.mail import send_mail 
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from datetime import date, datetime, timedelta


class CreateAttendanceAPIView(generics.CreateAPIView):
	"""
    API endpoint that allows Attandance to be created
    by the Authenticated Lecturer.
    """
	queryset = CreateAttendance.objects.all()
	serializer_class = CreateAttendanceSerializer
	code = id_generator()	

	def perform_create(self, serializer):
		created = datetime.now() + timedelta(minutes=int(serializer.validated_data.get('duration')))			
		serializer.save(user=self.request.user, code=self.code, created=created)

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			self.perform_create(serializer)
			response = {
            'success' : 'True',
            'message': f'Attendance created successfully. Code generated {self.code}',
        	}
		return Response(response, status=status.HTTP_200_OK)
	

class ListAttendanceAPIView(generics.ListAPIView):
	queryset = CreateAttendance.objects.all() 
	serializer_class = CreateAttendanceSerializer


class DeleteAttendanceAPIView(generics.DestroyAPIView):
	"""
    API endpoint that allows the Created Attendance sheet deleted.
    """
	queryset = CreateAttendance.objects.all() 
	serializer_class = CreateAttendanceSerializer


class FeedbackAPIView(generics.CreateAPIView):
	"""
    API endpoint that allows Users Feedback to be created
    by the Authenticated User.
    """
	queryset = Feedback.objects.all()
	serializer_class = FeedbackSerializer

	def perform_create(self, serializer):
		subject_ = serializer.data.get('subject')
		message_ = serializer.data.get('message')
        #Post to Database
		Feedback.objects.create(user = self.request.user, subject = subject_, message = message_)
        #Sent email to the Admin's GMAIL Account
		res = send_mail(subject_, message_, f'{self.request.user.email}', [f'{settings.EMAIL_HOST_USER}'])
		if res == 1:
			return Response("Feedback Received successfully!", status=status.HTTP_200_OK)
		else:  
			messages.debug(self.request, 'Mail could not sent') 
			Response("Mail could not be sent", status=status.HTTP_200_OK)
		serializer.save(user=self.request.user)


class TakeAttendanceAPIView(generics.CreateAPIView):
	"""
    API endpoint that allows Students Take Attendance.
    """
	serializer_class = TakeAttendanceSerializer

	def perform_create(self, serializer):
		code = serializer.data['code']
		current_time = datetime.now()
		qs = CreateAttendance.objects.filter(code=code, created__gt=current_time)
		if not qs.exists():
			raise serializers.ValidationError('Invalid Code')
		details = {
            'department': qs.first().department,
            'level': qs.first().level,
			'course': qs.first().course,
            'matric_no': self.request.user.student.matric_no,
			'lecturer': qs.first().user
        }
		print('Details Course________******', details['course'])
		print('Details Lecturer________******', details['lecturer'])
		if Attendance.objects.filter(
			student = self.request.user,
			lecturer = details['lecturer'],
			department = details['department'],
			level = details['level'],
			course = details['course'], 
			date = str(date.today())).count() != 0:
			raise serializers.ValidationError('Attendence already recorded.')
		else:
			students = Student.objects.filter(department=details['department'], level=details['level'])
			names = Recognizer(details)
			print("_______", names, "___________")
			for student in students:
				if str(student.matric_no) in names:
					attendance = Attendance(
						lecturer = details['lecturer'],
						student = self.request.user,
						matric_no = str(student.matric_no),
						department = details['department'],
						level = details['level'],
						present = 'Present')
					attendance.save()
				else:
					attendance = Attendance(
						lecturer = details['lecturer'],
						student = self.request.user,
						matric_no = str(student.matric_no),
						department = details['department'],
						level = details['level'])
					attendance.save()	
			return attendance

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			self.perform_create(serializer)			
			response = {
            'success' : 'True',
            'message': 'Attendance taken successfully.',
            'user' : f"{self.request.user}"
        }
		return Response(response, status=status.HTTP_200_OK)


class SearchAttendanceViewSet(viewsets.ModelViewSet):
	serializer_class = AttendanceSerializer
	queryset = Attendance.objects.all()
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter ]
	filterset_fields = ['date', 'id', "matric_no"]
	search_fields = ["matric_no", "date"]
	ordering_fields = '__all__'