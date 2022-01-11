from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth
from django.views.generic.base import RedirectView
from pages.models import Student , Attendance,AttendanceDetail,MarksDetail,Marks,Class,Course
from django.contrib.auth.decorators import login_required
from django.http import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

Dict={'student': None }

global current_studentid

# Create your views here.
@login_required(login_url='login')
def homeView(request,*args,**kwargs): 
    st=Student.objects.get(user_id=request.user.id)
    atn_obj=AttendanceDetail.objects.filter(student_id=request.user.id)
    totatt=atn_obj.count()
    student=atn_obj[0]
    presentatt=0
    absentatt=0
    for item in atn_obj:
        if item.status == True:
            presentatt += 1
        absentatt=totatt-presentatt
    Attendp=(presentatt/totatt)*100    

    #avg marks    
    current_student = Student.objects.get(user_id = request.user.id)
    department= Class.objects.get(class_id = current_student.class_id).dept_id_id
    Courses=Course.objects.filter(dept_id__id="CSX")
    Mst1=[]
    Mst2=[]
    Endsem=[]
    for item in Courses:
        code=item.course_id
        name=item.name
        target=MarksDetail.objects.filter(student_id=request.user.id).filter(marks__course_id=code)
        m1=0
        m2=0
        e=0
        for itr in target:
            m1=itr.mst1
            m2=itr.mst2
            e=itr.end_sem
        Mst1.append(m1)
        Mst2.append(m2)
        Endsem.append(e) 
    M1t=0
    M2t=0
    Endt=0    
    for list in Mst1:
        M1t += list
    M1t = M1t/len(Mst1)   
    M1t = round(M1t,2) 
        
    for list in Mst2:
        M2t+=list
    M2t = M2t/len(Mst2)  
    M2t = round(M2t,2)  

    for list in Endsem:
        Endt += list
    Endt = Endt/len(Endsem)
    Endt = round(Endt,2)
        
    context={
        'student':st,
        'mid1':M1t,
        'mid2':M2t,
        'ends':Endt, 
        'total':totatt,
        'present':presentatt,
        'absent':absentatt,
        'percent':Attendp
    }

    return render(request,"dashboard/index.html", context)

def login_user(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect(request, '/')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'loginform.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'loginform.html')         


@login_required(login_url='login')
def AttendanceView(request):
    current_student = Student.objects.get(user_id = request.user.id)
    

    studentobj=AttendanceDetail.objects.filter(student_id=request.user.id)
    totatt=studentobj.count()
    student=studentobj[0]
    presentatt=0
    absentatt=0
    for item in studentobj:
        if item.status == True:
            presentatt += 1
        absentatt=totatt-presentatt
    # course wise attendance
    department= Class.objects.get(class_id = current_student.class_id).dept_id_id
    Courses=Course.objects.filter(dept_id__id=department)
    CourseList=[]
    for item in Courses:
        code=item.course_id #dc101
        name=item.name #data communication
        target=AttendanceDetail.objects.filter(student_id=request.user.id).filter(attendance__course_id=code) 
        total=target.count()
        present=0
        absent=0
        for itr in target:
            if itr.status==True:
                present+=1
        absent=total-present
        percent=(present/total)*100
        CourseList.append([code,name,present,absent,percent])

    context={
        'CourseList':CourseList,
       
    }
    return render (request,"dashboard/attendance.html",context)


@login_required(login_url='login')
def Marksview(request):
    current_student = Student.objects.get(user_id = request.user.id)
    department= Class.objects.get(class_id = current_student.class_id).dept_id_id
    Courses=Course.objects.filter(dept_id__id="CSX")
    Markslist=[]
    for item in Courses:
        code=item.course_id
        name=item.name
        target=MarksDetail.objects.filter(student_id=request.user.id).filter(marks__course_id=code)
        m1=0
        m2=0
        e=0
        for itr in target:
            m1=itr.mst1
            m2=itr.mst2
            e=itr.end_sem
        Markslist.append([code,name,m1,m2,e])
    context={
        'Markslist':Markslist
    }
    return render(request,'dashboard/marks.html',context)


@login_required(login_url='login')
def Studentview(request):
    st=Student.objects.get(user_id=request.user.id)
    context={
        'student':st
    }
    return render(request,"dashboard/index.html",context)