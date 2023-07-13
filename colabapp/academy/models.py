from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Teacher(User):
    bio = models.CharField(max_length = 500, help_text = " Biography")

class Course(models.Model):
    name = models.CharField(max_length = 128)
    description = models.CharField(max_length = 500)

class Student(User):
    pass


class Subject (models.Model):
    course = models.ForeignKey(Course, on_delete = models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete = models.PROTECT)
    start_date = models.DateField()

class Subscription(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete = models.PROTECT)
    student_id = models.ForeignKey(Student, on_delete = models.PROTECT)
