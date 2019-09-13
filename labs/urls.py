from django.urls import path
from .views import CourseViewSet, LabViewSet, StudentViewSet, SessionViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('courses/', CourseViewSet.as_view(), name='courses'),
    path('labs/', LabViewSet.as_view(), name='labs'),
    path('session/', SessionViewSet.as_view({'get': 'list', 'post': 'create'}), name='session'),
    path('students/', StudentViewSet.as_view(), name='student')
]
