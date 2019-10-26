import datetime
from django.db import models
from django.contrib.auth.models import User


def current_year():
    return datetime.date.today().year


class Course(models.Model):
    SEMESTER_CHOICES = (
        (1, 'Sem1'),
        (2, 'Sem2'),
    )

    cid = models.CharField(max_length=6, primary_key=True)
    year = models.IntegerField(default=current_year)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=SEMESTER_CHOICES[1])
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return "%s-%s-%s-%s" % (self.year, self.get_semester_display(), self.cid, self.course_name)


class Lab(models.Model):
    lid = models.AutoField(primary_key=True)
    group = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs')
    instructors = models.ManyToManyField(User, related_name="labs")

    def __str__(self):
        return "%s-%s" % (self.course, self.group)


class Session(models.Model):
    sid = models.AutoField(primary_key=True)
    session_time = models.DateTimeField(auto_now_add=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, related_name="sessions")

    def __str__(self):
        return "%s %s" % (self.lab, self.session_time.strftime('%b %d %H:%M'))

    class Meta:
        ordering = ('session_time',)


class Student(models.Model):
    mid = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    face_encoding = models.BinaryField(blank=True)
    lab = models.ManyToManyField(Lab, related_name="students", blank=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    ATTENDANCE_STATUS = (
        ('A', "Attended"),
        ('L', "Late"),
        ('AB', "Absence without valid reasons"),
        ("MC", "Missing with valid reasons")
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=ATTENDANCE_STATUS, default='AB')
    reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s %s %s" % (self.session, self.student, self.get_status_display())

    class Meta:
        unique_together = (("student", "session"),)
