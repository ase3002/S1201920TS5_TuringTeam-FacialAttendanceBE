from django.urls import path
from .views import post_attendace_img, index, StudentFaceEncodingView, count_faces, end_session

urlpatterns = [
    path('', index, name='index'),
    path('count/', count_faces, name='count_faces'),
    path('face/', StudentFaceEncodingView.as_view(), name='student_face'),
    path('image/', post_attendace_img, name="attendance"),
    path('end/', end_session, name="end")
]
