from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models.deletion import CASCADE
from facial_app.api.manager import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from PIL import Image
import datetime

GENDER_CHOICE = (('Male','Male'),('Female','Female'))
LEVEL_CHOICE = (('100','100'),('200','200'),('300','300'),('400','400'),)
SEMESTER_CHOICE = (('First','First'),('Second','Second'))
DEPARTMENT  = (
        ('Computer Science','Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('Statistics','Statistics'),
        ('Physics', 'Physics'),
        ('Chemistry','Chemistry'),
        ('Biology','Biology'),
        ('Political Science','Political Science'),
        ('Economics','Economics'),
        ('Mass Communication','Mass Communication'),
        ('History','History'),
        ('English','English'),
    )
FACULTY = (('Science','Science'),('Social Science','Social Science'),('Arts','Arts'))

def upload_to(instance, filename):
    return 'profile_pics/{filename}'.format(filename=filename)

class User(AbstractUser):
    """CustomUser model."""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    objects = UserManager()
    contact = models.CharField(validators = [RegexValidator(regex = r"^\+?1?\d{8,15}$")], max_length = 16)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=34, default='Male')    
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    signup_confirmation = models.BooleanField(default=False) 
    avatar = models.ImageField(_('Image'), upload_to=upload_to, default='default.png')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        try:
            image = Image.open(self.avatar.path)
            if image.height > 300 or image.width > 300:
                image.thumbnail((150,150))
                image.save(self.avatar.path)   
        except:
            print("******Error in Processing images*******")
            return        
    
    @property
    def get_photo_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return "/static/default.png"

    def __str__(self):
        return f'{self.email}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='student')
    matric_no = models.CharField(max_length=15)
    semester = models.CharField(choices=SEMESTER_CHOICE, max_length=10, default='First')
    level = models.CharField(choices=LEVEL_CHOICE, max_length=5, default='100')
    dob = models.DateField(max_length=23)
    department = models.CharField(choices=DEPARTMENT, max_length=30, default='Computer Science')
    
    def __str__(self):
        return f'{self.matric_no}'
    

class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='lecturer')
    department = models.CharField(choices=DEPARTMENT, max_length=30, default='Computer Science')
    faculty = models.CharField(choices=FACULTY, max_length=30, default='Science')

    def __str__(self):
        return f'{self.user.get_full_name()} | {self.department}'


class Attendance(models.Model):
    lecturer = models.ForeignKey(User, on_delete=CASCADE, related_name='user_lecturer')
    student = models.ForeignKey(User, on_delete=CASCADE)
    matric_no = models.CharField(max_length=200, null=True, blank=True)
    department = models.CharField(max_length=200, null=True, blank=True)
    level = models.CharField(max_length=200, null=True, blank=True)
    course = models.CharField(null=True, max_length=6)
    date = models.DateField(auto_now_add = True, null = True)
    time = models.TimeField(auto_now_add=True, null = True)
    present = models.CharField(default="Absent", max_length=10)

    def __str__(self):
        return f"{self.student} | {self.department}"


class CreateAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    title = models.CharField(max_length=100)
    level = models.CharField(choices=LEVEL_CHOICE, max_length=5, default='100')
    department = models.CharField(choices=DEPARTMENT, max_length=30, default='Computer Science')
    course = models.CharField(max_length=10)
    duration = models.PositiveIntegerField(default=2, validators=[MinValueValidator(2), MaxValueValidator(10)])
    created = models.DateTimeField(null=True)
    code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user} | {self.title}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    subject = models.CharField(max_length=40)
    message = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} | {self.subject}'

