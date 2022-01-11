from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from .models import Attendance, Course, MarksDetail, Student, Department, Class, AttendanceDetail, Marks

# Register your models here.

'''
class UserAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'name']
    search_fields = ['course_id', 'name']
'''

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0

class ClassesAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ['class_id', 'section', 'semester', 'dept_id']
    search_fields = ['class_id', 'section', 'semester', 'dept_id__name']
    ordering = ['class_id']


class ClassInLine(admin.TabularInline): # To add tabluar class model in Departments page in django admin
    model = Class
    extra = 0
    # A foreign key field is not rendered inside an inline model admin in django

class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_id', 'dept_id']
    fields = ['course_id', 'name', 'dept_id']
    search_fields = ['name', 'course_id', 'dept_id__name']
    ordering = ['name']

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [ClassInLine]
    list_display = ['name', 'id'] # Fields of Department table
    search_fields = ['name', 'id'] # Fields of Department table
    ordering = ['name']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'enrollment_no', 'name', 'class_id', 'dob', 'gender']
    search_fields = ['user_id__username', 'enrollment_no', 'name']
    fields = ['user_id', 'enrollment_no', 'name', 'class_id', 'dob', 'gender']
    ordering = ['enrollment_no']

class MarksInLine(admin.TabularInline):
    model = MarksDetail
    extra = 0

class MarksAdmin(admin.ModelAdmin):
    inlines = [MarksInLine]
    list_display = ['course_id', 'class_id']
    search_fields = ['course_id__name', 'class_id__class_id']
    ordering = ['class_id']


class AttendanceInline(admin.TabularInline):
    model = AttendanceDetail
    extra = 0
    fields = ['student_id', 'status']


class AttendanceAdmin(admin.ModelAdmin):
    inlines = [AttendanceInline]
    list_display = ['course_id', 'attendance_date']
    fields = ['course_id', 'attendance_date']
    search_fields = ['course_id__name', 'attendance_date']
    ordering = ['attendance_date']

    def get_enrollno(self, obj):
        return obj.student_id.enrollment_no
    get_enrollno.short_description = 'Enrollment Number'
    get_enrollno.admin_order_field = 'student_id__enrollment_no'


# class ClassCourseInline(admin.TabularInline):
#     model = Course
#     extra = 0
#     fields = ['name']

# class ClassCourseAdmin(admin.ModelAdmin):
#     inlines = [ClassCourseInline]
#     list_display = ['class_id']
#     search_fields = ['class_id']
#     ordering = ['class_id']

# admin.site.register(User, UserAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Class, ClassesAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(ClassCourse, ClassCourseAdmin)
admin.site.register(Marks, MarksAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department, DepartmentAdmin)
