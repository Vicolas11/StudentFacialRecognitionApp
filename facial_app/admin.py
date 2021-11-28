from facial_app.models import (Attendance, CreateAttendance, Feedback, Lecturer, Student, User)
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','gender','contact','avatar',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','is_lecturer','is_student',
                                    'signup_confirmation',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )
    list_display = ('id','email','username','first_name', 'last_name', 'is_staff','gender','contact')
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-id',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','matric_no','level','department','semester','dob',)}),
    )
    list_display = ('id','user','matric_no','level', 'department','dob')
    search_fields = ('id','level', 'matric_no', 'department',)
    ordering = ('-id',)


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','department','faculty')}),
    )
    list_display = ('id','user','department','faculty')
    search_fields = ('id','user','department','faculty',)
    ordering = ('-id',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('student','matric_no','department','level','date','time','present')}),
    )
    list_display = ('id','student','matric_no','department','level','date','time','present')
    search_fields = ('id','student','department','matric_no','date','present')
    ordering = ('-id',)


@admin.register(CreateAttendance)
class CreateAttendanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','title','code','department','level','course','created',)}),
    )
    list_display = ('id','user','title','code','department','level','course','created',)
    search_fields = ('id','user','title','department','matric_no','code',)
    ordering = ('-id',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('user','subject','message','created',)}),
    )
    list_display = ('id','user','subject','message','created',)
    search_fields = ('id','user','subject','created',)
    ordering = ('-id',)
