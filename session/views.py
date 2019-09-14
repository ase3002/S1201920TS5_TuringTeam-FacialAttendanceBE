import os
import json
import numpy as np

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from rest_framework.exceptions import ParseError
from PIL import Image
import face_recognition
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from .session_manager import handle_recognition_request

IMG_PATH = 'images'
counter = 0


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def post_attendace_img(request):
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


@csrf_exempt
def index(request):
    json_data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        n_faces = handle_recognition_request(json_data)
        return JsonResponse({"n_faces": n_faces})
    return HttpResponseBadRequest("Bad Request")
