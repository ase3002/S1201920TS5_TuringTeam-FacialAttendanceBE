from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Lab, Student, Session, Attendance
from .serializers import CourseSerializer, LabSerializer, StudentSerializer, SessionSerializer, AttendanceSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


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
    filterset_fields = ['lab']


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filterset_fields = ['student', 'session']


class SessionsByLId(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    filterset_fields = ['lab']


def sessionBySId(request, *args, **kwargs):
    session = get_object_or_404(Session, sid=kwargs['sid'])
    attendance = Attendance.objects.filter(session=kwargs['sid'])\
        .values('student', 'session', 'status', 'reason', 'student__name')

    return JsonResponse(dict(
        sid=session.sid,
        time=session.session_time,
        students=[dict(mid=a['student'], name=a['student__name'], attendance=a['status'], remark=a['reason']) for a in attendance]))


def studentByMid(request, *args, **kwargs):
    student = get_object_or_404(Student, mid=kwargs['mid'])
    attendance = Attendance.objects.filter(student=kwargs['mid'])\
        .values('session', 'status', 'reason')

    return JsonResponse(dict(
        mid=student.mid,
        name=student.name,
        email=student.email,
        sessions=[dict(sid=a['session'], attendance=a['status'], remark=a['reason']) for a in attendance]))


@api_view(['POST'])
def updateAttendanceBySId(request, *args, **kwargs):
    for std in request.data['students']:
        Attendance.objects.update_or_create(
            student=Student.objects.get(mid=std['mid']),
            session=Session.objects.get(sid=int(request.data['sid'])),
            defaults=dict(
                status=std['attendance'],
                reason=std['remark']))

    return Response(request.data['sid'], status=status.HTTP_200_OK)


@api_view(['POST'])
def updateAttendanceByMId(request, *args, **kwargs):
    for session in request.data['sessions']:
        Attendance.objects.update_or_create(
            student=Student.objects.get(mid=request.data['mid']),
            session=Session.objects.get(sid=int(session['sid'])),
            defaults=dict(
                status=session['attendance'],
                reason=session['remark']))

    return Response(request.data['mid'], status=status.HTTP_200_OK)
