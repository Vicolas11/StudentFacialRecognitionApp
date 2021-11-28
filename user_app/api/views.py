from facial_app.video_capture import video_capture
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from facial_app.models import Lecturer, User
from rest_framework.parsers import FormParser, MultiPartParser
from user_app.api.serializers import (ChangePasswordSerializer, LecturerLoginSerializer, LecturerProfileUpdateSerializer, LecturerRegistrationSerializer, StudentLoginSerializer, StudentProfileUpdateSerializer, StudentRegistrationSerializer, UserAvatarSerializer)
from rest_framework import serializers, status, authentication
from django.contrib import messages
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from user_app.token import account_activation_token
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LecturerRegistrationView(CreateAPIView):
    serializer_class = LecturerRegistrationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)   
        if serializer.is_valid():
            user = serializer.save()
            if user is not None:
                user.refresh_from_db()
                user.is_active = False
                user.save()
                #Send an activation email to the user once signup
                subject = 'Verify your account'
                use_https = self.request.is_secure(),
                current_site = get_current_site(self.request)            
                msg = render_to_string('activate.html', {
                    'user': user,
                    'protocol': 'https' if use_https else 'http',
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
                res = send_mail(
                    subject=subject, 
                    message=msg,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email])
                if res == 1:
                    response = {
                    'success' : 'True',
                    'message': 'Registered successfully! Check your email for activation! Check spam please!',
                    'user': serializer.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    messages.success(request, 'Email not sent. Account not registered!') 
        else:
            messages.error(request, serializer.errors)      
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRegistrationView(CreateAPIView):
    """
    This API EndPoint Register a new Student User
    """
    serializer_class = StudentRegistrationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)   
        if serializer.is_valid():
            user = serializer.save()
            video_capture(serializer.data['student']['department'],serializer.data['student']['level'],serializer.data['student']['matric_no'])
            if user is not None:
                user.refresh_from_db()
                user.is_active = False
                user.save()
                #Send an activation email to the user once signup
                subject = 'Verify your FaceAttendanceApp Account'
                use_https = self.request.is_secure(),
                current_site = get_current_site(self.request)            
                msg = render_to_string('activate.html', {
                    'user': user,
                    'protocol': 'https' if use_https else 'http',
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'link': "<a>"+ f"{self.request.scheme }://{self.request.get_host}user/api/activate/uidb64={urlsafe_base64_encode(force_bytes(user.pk))}/token={account_activation_token.make_token(user)}" + "</a>"
                })
                res = send_mail(
                    subject=subject, 
                    message=msg,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email])
                if res == 1:
                    response = {
                    'success' : 'True',
                    'message': 'Registered successfully! Please Check your email for activation! Check spam incase',
                    'user': serializer.data
                    }
                    
                    return Response(response, status=status.HTTP_201_CREATED)
                else:
                    messages.success(request, 'Email not sent. Account not registered!') 
                    return Response({'message', 'Email not sent. Account not registered!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            messages.error(request, serializer.errors)      
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Validate and Activate New Sign Lead
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        #Activate the user after clicking the link
        user.is_active = True
        user.signup_confirmation = True
        user.save()
        return redirect('activated_completed')
    else:
        messages.error(request, f'Account activated unsuccessfully!')
        return redirect('activation_invalid')


class UserAvatarUpload(CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def post(self, request, format=None):
        instance = self.get_object()
        serializer = UserAvatarSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LecturerProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = LecturerProfileUpdateSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Profile Updated Succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentProfileUpdateSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Profile Updated Succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LecturerLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LecturerLoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__iexact=serializer.data['email'])
        login(request, user)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'user' : serializer.data['email']
        }
        status_code = status.HTTP_200_OK
        messages.success(request, 'Login Successfully')
        return Response(response, status=status_code)


class StudentLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = StudentLoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email__iexact=serializer.data['email'])
        login(request, user)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'user' : serializer.data['email']
        }
        status_code = status.HTTP_200_OK
        messages.success(request, 'Login Successfully')
        return Response(response, status=status_code)


#For Test Purpose Delete Later
class UsersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = LecturerRegistrationSerializer

"""
class PasswordResetView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            serializer.save(**opts)
            return Response({"message":"PasswordRest link sent!"}, status=status.HTTP_200_OK)
"""

class LogoutView(APIView):

    def post(self, request):
        logout(request)
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User Successfully Logout!'
        }
        return response


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Updated Succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)