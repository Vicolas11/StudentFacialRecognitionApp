from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from facial_app.models import Lecturer, Student, User
from django.conf import settings


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["avatar",]

    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(*args, **kwargs)


class StudentSerializer(serializers.ModelSerializer):
    matric_no = serializers.CharField(required=False)
    department = serializers.CharField(required=False)

    class Meta:
        model = Student
        fields = ('matric_no', 'semester', 'level', 'dob', 'department',)


class StudentRegistrationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)
    
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'gender', 'contact',
                'student', 'is_student', 'is_lecturer', 'signup_confirmation',)
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, attrs, *args, **kwargs):
        matric_no = attrs['student']['matric_no']
        user_query = Student.objects.filter(matric_no__iexact=matric_no).exists()
        if user_query:
            raise serializers.ValidationError(f'{matric_no} already exist!')
        return super(StudentRegistrationSerializer, self).validate(attrs, *args, **kwargs) 

    def create(self, validated_data):
        student_data = validated_data.pop('student', None)
        user = User.objects.create_user(**validated_data)
        Student.objects.create(
            user=user,
            matric_no=student_data['matric_no'],
            semester=student_data['semester'],
            level=student_data['level'],
            dob=student_data['dob'],
            department=student_data['department']
        )
        return user


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs, *args, **kwargs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        qs = User.objects.filter(email__iexact=email).exists()
        if qs is None:
            raise serializers.ValidationError(f'Sorry {email} does not exist.')
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')
        if not user.is_active:
            raise serializers.ValidationError('Sorry your account has not been verified.')
        if not user.is_student:
            raise serializers.ValidationError(f'Sorry {email} is not a student account.')
        return super(StudentLoginSerializer, self).validate(attrs, *args, **kwargs)


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    student = StudentSerializer(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'contact','student',)

    def update(self, instance, validated_data):
        student_data = validated_data.pop('student', None)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.gender = validated_data['gender']
        instance.contact = validated_data['contact']
        if student_data is not None:
            instance.student.semester = student_data['semester']
            instance.student.level = student_data['level']
            instance.student.dob = student_data['dob']           
            instance.student.save()
        instance.save()
        return super(StudentProfileUpdateSerializer, self).update(instance, validated_data)


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ('department','faculty',) 


class LecturerRegistrationSerializer(serializers.ModelSerializer):
    lecturer = LecturerSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'gender', 'contact',
                'lecturer', 'is_student', 'is_lecturer', 'signup_confirmation')
        extra_kwargs = {'password': {'write_only': True}}   
    
    def validate_email(self, data):
        user_query = User.objects.filter(email__iexact=data).exists()
        if user_query:
            raise serializers.ValidationError(f'{data} already exist!')
        return data

    def create(self, validated_data):
        lecturer_data = validated_data.pop('lecturer', None)
        user = User.objects.create_user(**validated_data)
        if lecturer_data:
            Lecturer.objects.create(
                user=user,
                department=lecturer_data['department'],
                faculty=lecturer_data['faculty']
            )
        return user


class LecturerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs, *args, **kwargs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        qs = User.objects.filter(email__iexact=email).exists()
        if qs is None:
            raise serializers.ValidationError(f'Sorry {email} does not exist.')
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')
        if not user.is_active:
            raise serializers.ValidationError('Sorry your account has not been verified.')
        if not user.is_lecturer:
            raise serializers.ValidationError(f'Sorry {email} is not a lecturer account.')
        return super(LecturerLoginSerializer, self).validate(attrs, *args, **kwargs)

class LecturerProfileUpdateSerializer(serializers.ModelSerializer):
    lecturer = LecturerSerializer(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'contact','lecturer',)

    def update(self, instance, validated_data):
        lecturer_data = validated_data.pop('lecturer', None)
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.gender = validated_data['gender']
        instance.contact = validated_data['contact']
        if lecturer_data is not None:
            instance.lecturer.department = lecturer_data['department']
            instance.lecturer.faculty = lecturer_data['faculty']
            instance.lecturer.save()
        instance.save()
        return super(LecturerProfileUpdateSerializer, self).update(instance, validated_data)

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Password fields didn't match.")
        return super(ChangePasswordSerializer, self).validate(attrs)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return super(ChangePasswordSerializer, self).validate(value)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance   
    