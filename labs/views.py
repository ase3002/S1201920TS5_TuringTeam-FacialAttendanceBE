from rest_framework import status, views, viewsets, permissions, generics
from .models import Course, Lab, Student, Session, Attendance
from .serializers import CourseSerializer, LabSerializer, StudentSerializer, SessionSerializer, AttendanceSerializer


class CourseViewSet(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LabListView(generics.ListAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    filterset_fields = ['instructors']


class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ['labs']


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filterset_fields = ['student', 'session']
