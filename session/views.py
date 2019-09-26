import os
import json
import numpy as np
import pickle
import base64

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from rest_framework.exceptions import ParseError
from PIL import Image
import face_recognition
from rest_framework import status, views, parsers, exceptions
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.decorators import api_view, parser_classes
from .session_manager import handle_recognition_request
from labs.models import Student, Session, Lab

IMG_PATH = 'images'
counter = 0

face_data = {}


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def count_faces(request):
    if 'file' not in request.data:
        raise ParseError("Empty Content")

    f = request.data['file']
    # verify image
    im = Image.open(f)
    im.verify()

    # open image
    im = Image.open(f)
    # if not os.path.exists(IMG_PATH):
    #     os.mkdir(IMG_PATH)
    # im.save(os.path.join(IMG_PATH, 'photo.jpg'))

    im = im.convert('RGB')
    image = np.array(im)
    n_faces = len(face_recognition.face_locations(image))

    global counter
    counter += 1
    return Response(n_faces, status=status.HTTP_200_OK)


@api_view(['POST'])
def end_session(request, *args, **kwargs):
    if 'sid' not in request.data:
        raise ParseError('No sid found')

    sid = request.data['sid']
    if sid in face_data:
        del face_data[sid]
        return Response(sid, status=status.HTTP_200_OK)
    return HttpResponseBadRequest('Session not started')


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def post_attendace_img(request, *args, **kwargs):
    if 'image' not in request.data:
        raise ParseError('No image')

    if 'sid' not in request.data:
        raise ParseError('Not sid found')

    f = request.data['image']
    try:
        im = Image.open(f)
        im.verify()
    except Exception:
        raise exceptions.ParseError("Unsupported image")

    im = Image.open(f)
    im = im.convert('RGB')
    im = np.array(im)
    sid = request.data['sid']
    face_locations = face_recognition.face_locations(im)
    face_encodings = face_recognition.face_encodings(im, face_locations)

    global face_data
    if sid not in face_data:
        session = Session.objects.get(pk=sid)
        students = session.lab.students.all()
        known_face_encodings = [pickle.loads(base64.b64decode(student.face_encoding)) for student in students]
        known_face_matric = [student.matric_num for student in students]
        face_data[sid] = {
            'known_face_encodings': known_face_encodings,
            'known_face_matric': known_face_matric,
            'all_students_matric': [student.matric_num for student in students]
        }

    known_face_encodings = face_data[sid]['known_face_encodings']
    known_face_matric = face_data[sid]['known_face_matric']
    all_students_matric = face_data[sid]['all_students_matric']

    attended_matric = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = 'Unknown'

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_matric[best_match_index]
            attended_matric.append(name)

    status = ['attend' if matric in attended_matric else 'missing' for matric in all_students_matric]
    result = {'result': list(zip(all_students_matric, status))}
    return JsonResponse(result)


@csrf_exempt
def index(request):
    json_data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        n_faces = handle_recognition_request(json_data)
        return JsonResponse({"n_faces": n_faces})
    return HttpResponseBadRequest("Bad Request")


class StudentFaceEncodingView(views.APIView):
    parser_class = (parsers.FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'image' not in request.data:
            raise exceptions.ParseError("No image found")
        if 'matric' not in request.data:
            raise exceptions.ParseError("No matric found")

        f = request.data['image']

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

        sid = request.data['matric']
        try:
            student = Student.objects.get(pk=sid)
            student.face_encoding = face_encoding_base64
            student.save()
        except Exception:
            return Response('Error occured', status=status.HTTP_400_BAD_REQUEST)

        return Response(sid, status=status.HTTP_200_OK)
