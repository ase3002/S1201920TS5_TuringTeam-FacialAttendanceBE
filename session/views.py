import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm

import face_recognition

from .session_manager import handle_recognition_request

@csrf_exempt
def index(request):
    json_data = json.loads(request.body.decode("utf-8"))
    if request.method == 'POST':
        n_faces = handle_recognition_request(json_data)
        return JsonResponse({"n_faces": n_faces})
    return HttpResponseBadRequest("Bad Request")
    