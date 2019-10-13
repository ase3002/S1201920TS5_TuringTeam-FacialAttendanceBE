from django.urls import path
from .views import CourseViewSet, LabListView, StudentListView, SessionViewSet, AttendanceViewSet, SessionsByLId, sessionBySId, studentByMid, updateAttendanceBySId, updateAttendanceByMId
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('courses/', CourseViewSet.as_view(), name='courses'),
    path('labs/', LabListView.as_view(), name='labs'),
    path('session/', SessionViewSet.as_view({'get': 'list', 'post': 'create'}), name='session'),
    path('students/', StudentListView.as_view(), name='student'),
    path('sessions/', SessionsByLId.as_view()),
    path('session/<int:sid>', sessionBySId),
    path('student/<str:mid>', studentByMid),
    path('attendance/session', updateAttendanceBySId),
    path('attendance/student', updateAttendanceByMId)
]

urlpatterns.extend(router.urls)
