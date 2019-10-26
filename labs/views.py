from PIL import Image
from rest_framework import status, viewsets, generics, views, parsers, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course, Lab, Student, Session, Attendance
from .serializers import CourseSerializer, LabSerializer, StudentSerializer, SessionSerializer, AttendanceSerializer
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

import base64
import pickle
import face_recognition
import numpy as np


def encode_facedata(f):
    try:
        im = Image.open(f)
        im.verify()
    except Exception:
        raise exceptions.ParseError("Unsupported image")
    im = Image.open(f)
    face_image = np.array(im.convert('RGB'))
    face_encoding = face_recognition.face_encodings(face_image)[0]
    face_encoding_bytes = pickle.dumps(face_encoding)
    face_encoding_base64 = base64.b64encode(face_encoding_bytes)
    return face_encoding_base64


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

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            # save face encoding data
            if 'image' in request.data:
                f = request.data['image']
                face_encoding_base64 = encode_facedata(f)
                student.face_encoding = face_encoding_base64
                student.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(views.APIView):
    def _get_object(self, mid):
        try:
            return Student.objects.get(mid=mid)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, mid, format=None):
        student = get_object_or_404(Student, mid=mid)
        attendance = Attendance.objects.filter(student=mid)\
            .values('session', 'status', 'reason')

        return JsonResponse(dict(
            mid=student.mid,
            name=student.name,
            email=student.email,
            sessions=[dict(sid=a['session'], attendance=a['status'], remark=a['reason']) for a in attendance]))

    def put(self, request, mid, format=None):
        student = self._get_object(mid)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            if 'image' in request.data:
                f = request.data['image']
                face_encoding_base64 = encode_facedata(f)
                student.face_encoding = face_encoding_base64
                student.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, mid, format=None):
        student = self._get_object(mid)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
