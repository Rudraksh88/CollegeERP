from typing import Coroutine
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.enums import Choices
from django.db.models.fields import *
from django.db.models.fields.related import ForeignKey
from django.http import request

gender = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length = 50)
    id   = models.CharField(primary_key = 'True', verbose_name = 'Department ID', max_length = 20)

    def __str__(self):
        return self.name


class Class(models.Model): 
    class_id = models.CharField(primary_key='True', max_length=20, verbose_name='Class ID')
    section  = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    dept_id  = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name = 'Department')

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.class_id

# class ClassCourse(models.Model):
#     class_id = models.ForeignKey(Class, on_delete=DO_NOTHING)

class Course(models.Model):
    course_id = models.CharField(primary_key = 'True', max_length = 20, verbose_name = 'Course ID')
    dept_id   = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name = 'Course Department')
    name      = models.CharField(max_length = 50, verbose_name= 'Course Name')
    # classcourse = models.ForeignKey(ClassCourse, on_delete=DO_NOTHING)

    # Displays the actual model name instead of <x object> in django admin page
    def __str__(self):
        return self.name


class Student(models.Model):
    user_id       = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length = 15, verbose_name='Enrollment Number')
    class_id      = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name= 'Class')
    name          = models.CharField(max_length=50, verbose_name='Name')
    dob           = models.DateField(verbose_name='Date of Birth')
    gender        = models.CharField(max_length=10,choices = gender,verbose_name='Gender')

    def __str__(self):
        return self.name


class Marks(models.Model):
    #student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id  = models.ForeignKey(Course, on_delete=DO_NOTHING)
    class_id = models.ForeignKey(Class, on_delete=DO_NOTHING)

    class Meta:
        verbose_name_plural = 'Marks'
    

class MarksDetail(models.Model):
    student_id = models.ForeignKey(Student, on_delete=DO_NOTHING)
    marks      = models.ForeignKey(Marks, on_delete=models.CASCADE)
    # class_id   = models.ForeignKey(Class, on_delete=DO_NOTHING)
    mst1       = models.IntegerField()
    mst2       = models.IntegerField()
    end_sem    = models.IntegerField()

    def __str__(self):
        return 'Marks in exam'


class Attendance(models.Model):
    # student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=DO_NOTHING)
    attendance_date = models.DateField()

    class Meta:
        verbose_name_plural = 'Attendance'

    def __str__(self):
        return self.course_id.name


class AttendanceDetail(models.Model):
    student_id = models.ForeignKey(Student, on_delete=DO_NOTHING)
    # course_id  = models.ForeignKey(Course, on_delete=DO_NOTHING) 
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status     = models.BooleanField(default=True, null= False)
    # date       = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):  
        return 'Attendance' + ' ' + self.student_id.name
        #return 'Attendance in' + ' ' + self.attendance.course_id.name


# class Teacher(models.Model):
#     user       = models.OneToOneField(User, on_delete=models.CASCADE, null= True)
#     teacher_id = models.CharField(primary_key = 'True', max_length = 20, verbose_name='Teacher ID')
#     dept       = models.ForeignKey(Department, on_delete=models.CASCADE)
#     name       = models.CharField(max_length = 50)
#     gender     = models.CharField(max_length = 10, choices = gender)
#     DOB        = models.DateField()

#     def __str__(self):
#         return self.name


# class Marks(models.Model):
#     student      = models.ForeignKey(Student, on_delete=DO_NOTHING, primary_key=True)
#     course       = models.ForeignKey(StudentCourse, on_delete=DO_NOTHING)

#     class Meta:
#         verbose_name_plural='Marks'


# TODO @login required // DONE
# TODO request user - make a custom user model for request.user.enrollment_no instead of request.user.id
# TODO sender signal from user to student model
# TODO Use data from database and display useful info (attendance, marks, etc.)
# TODO get data from login/sign-up form
# TODO user image field in user model (optional)

