from rest_framework import status, views, viewsets, permissions, generics
from .models import Course, Lab, Student, Session
from .serializers import CourseSerializer, LabSerializer, StudentSerializer, SessionSerializer


class CourseViewSet(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LabViewSet(generics.ListAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer
    filterset_fields = ['instructors']


class StudentViewSet(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ['labs']


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
