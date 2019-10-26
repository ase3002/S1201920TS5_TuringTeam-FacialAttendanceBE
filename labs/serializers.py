from rest_framework import serializers
from .models import Course, Lab, Student, Session, Attendance


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lab
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    labs = serializers.PrimaryKeyRelatedField(queryset=Lab.objects.all(), many=True, source="lab")

    class Meta:
        model = Student
        fields = ('mid', 'name', 'email', 'labs')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        exclude = ('id',)
