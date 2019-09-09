from django.contrib import admin
from .models import Course, Lab, Session, Student, Attendance

admin.site.register(Course)
admin.site.register(Lab)
admin.site.register(Session)
admin.site.register(Student)
admin.site.register(Attendance)
