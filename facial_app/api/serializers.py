from facial_app.models import Attendance, CreateAttendance, Feedback, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreateAttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    title = serializers.CharField(max_length=20)
    code = serializers.CharField(required=False)
    created =serializers.DateTimeField(required=False)

    class Meta:
        model = CreateAttendance
        fields = ('user','title','level','department','course','code','duration','created')
    
    def validate(self, attrs, *args, **kwargs):
        qs = CreateAttendance.objects.filter(title=attrs['title']).exists()
        if qs:
            raise serializers.ValidationError("Attendance created already")
        return super(CreateAttendanceSerializer, self).validate(attrs, *args, **kwargs)


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'


class TakeAttendanceSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validated_code(self, value):
        qs = CreateAttendance.objects.get(code=value)
        if qs is None:
            raise serializers.ValidationError("Invalid Code")
        return value


class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Feedback
        fields = ('user','subject','message',)