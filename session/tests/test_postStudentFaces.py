from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from labs.models import Student

import os


class TestStudentFaceEncodingView(TestCase):
    def setUp(self):
        self.student = Student.objects.create(mid='U1622102L', name='test',
                                              email='test@example')
        self.client = Client()
        User.objects.create_user(username='admin', email='admin@example.com', password='adminpassword')
        self.client.login(username='admin', password='adminpassword')

    def testPostStudentFaceImageSuccess(self):
        with open(os.path.join(os.path.dirname(__file__), 'studentImage1.jpg'), 'rb') as f:
            response = self.client.post(reverse('student_face'), {'mid': 'U1622102L', 'image': f})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.student.mid)
