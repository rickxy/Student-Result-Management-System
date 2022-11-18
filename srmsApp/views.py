from turtle import clear
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from srmsApp import forms, models

context={
    'page':'',
    'page_title':'',
    'system_name':'Student Result Managament System',
    'short_name':'SRMS',
    'has_navigation':True,
    'has_sidebar':True,
}
# Create your views here.
@login_required
def home(request):
    context['page'] = 'home'
    context['page_title'] = 'Dashboard'
    context['classes'] = models.Class.objects.filter(status =1).count()
    context['subjects'] = models.Subject.objects.filter(status =1).count()
    context['students'] = models.Student.objects.filter(status =1).count()
    context['results'] = models.Result.objects.count()
    context['has_navigation'] = True
    context['has_sidebar'] = True
    return render(request,'home.html',context)

#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(student):
    logout(student)
    return redirect('/')


@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)

@login_required
def profile(request):
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request,'profile.html', context)


# Class
@login_required
def class_mgt(request):
    context['page'] = 'class_mgt'
    context['page_title'] = 'Class Management'
    classes = models.Class.objects.all()
    context['classes'] = classes
    return render(request,'class_mgt.html',context)


@login_required
def manage_class(request, pk = None):
    if not pk is None:
        classData = models.Class.objects.get(id = pk)
        context['classData'] = classData
    else:
        context['classData'] = {}
    return render(request, 'manage_class.html', context)

@login_required
def save_class(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveClass(post)
        else:
            _class = models.Class.objects.get(id = post['id'])
            form = forms.SaveClass(post, instance=_class)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "Class Detail has been saved successfully.")
        else:
            resp['msg'] = 'Class Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str("<br/>"+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_class(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Class.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "Class Detail has been deleted successfully.")
        except:
            resp['msg'] = 'Class Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")



#Subject
@login_required
def subject_mgt(request):
    context['page'] = 'subject_mgt'
    context['page_title'] = 'Subject Management'
    subjects = models.Subject.objects.all()
    context['subjects'] = subjects
    return render(request,'subject_mgt.html',context)


@login_required
def manage_subject(request, pk = None):
    if not pk is None:
        subject = models.Subject.objects.get(id = pk)
        context['subject'] = subject
    else:
        context['subject'] = {}
    return render(request, 'manage_subject.html', context)

@login_required
def view_subject(request, pk = None):
    if not pk is None:
        subject = models.Subject.objects.get(id = pk)
        context['subject'] = subject
    else:
        context['subject'] = {}
    return render(request, 'view_subject.html', context)

@login_required
def save_subject(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveSubject(post)
        else:
            subject = models.Subject.objects.get(id = post['id'])
            form = forms.SaveSubject(post, instance=subject)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "Subject Detail has been saved successfully.")
        else:
            resp['msg'] = 'Subject Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(f"<br/>"+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_subject(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Subject.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "Subject Detail has been deleted successfully.")
        except:
            resp['msg'] = 'Subject Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")

#Students
@login_required
def student_mgt(request):
    context['page'] = 'student_mgt'
    context['page_title'] = 'Student Management'
    students = models.Student.objects.all()
    context['students'] = students
    return render(request,'student_mgt.html',context)


@login_required
def manage_student(request, pk = None):
    classes = models.Class.objects.filter(status = 1).all()
    context['classes'] = classes
    if not pk is None:
        student = models.Student.objects.get(id = pk)
        context['student'] = student
    else:
        context['student'] = {}
    return render(request, 'manage_student.html', context)

@login_required
def view_student(request, pk = None):
    if not pk is None:
        student = models.Student.objects.get(id = pk)
        context['student'] = student
    else:
        context['student'] = {}
    return render(request, 'view_student.html', context)

@login_required
def save_student(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveStudent(post)
        else:
            student = models.Student.objects.get(id = post['id'])
            form = forms.SaveStudent(post, instance=student)

        if form.is_valid():
            form.save()
            resp['status'] = 'success'
            messages.success(request, "Student Detail has been saved successfully.")
        else:
            resp['msg'] = 'Student Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(f"<br/> [{field.name}] "+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_student(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Student.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "Student Detail has been deleted successfully.")
        except:
            resp['msg'] = 'Student Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")

#Result
@login_required
def result_mgt(request):
    context['page'] = 'result_mgt'
    context['page_title'] = 'Result Management'
    results =models.Result.objects.all()
    context['results'] = results
    return render(request,'result_mgt.html',context)


@login_required
def manage_result(request, pk = None):
    students = models.Student.objects.filter(status = 1).all()
    context['students'] = students
    subjects = models.Subject.objects.filter(status = 1).all()
    context['subjects'] = subjects
    if not pk is None:
        result =models.Result.objects.get(id = pk)
        marks =models.Student_Subject_Result.objects.filter(result = result)
        context['marks'] = marks
        context['result'] = result
    else:
        context['result'] = {}
        context['marks'] = {}
    return render(request, 'manage_result.html', context)

def view_result(request, pk = None):
    if not pk is None:
        result =models.Result.objects.get(id = pk)
        context['result'] = result
        marks =models.Student_Subject_Result.objects.filter(result = result)
        context['marks'] = marks
    else:
        context['result'] = {}
        context['marks'] = {}
    return render(request, 'view_result.html', context)

@login_required
def save_result(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        if post['id'] == None or post['id'] == '':
            form = forms.SaveResult(post)
        else:
            result =models.Result.objects.get(id = post['id'])
            form = forms.SaveResult(post, instance=result)
        if form.is_valid():
            form.save()
            is_new = False
            if post['id'] == '':
                rid = models.Result.objects.all().last().id
                result =models.Result.objects.get(id = rid)
                is_new = True
            else:
                rid = post['id']
            models.Student_Subject_Result.objects.filter(result = result).delete()
            has_error = False
            subjects= request.POST.getlist('subject[]')
            grade= request.POST.getlist('grade[]')
            i = 0
            for subject in subjects:
                data = {
                    'result' :rid,
                    'subject' :subject,
                    'grade' : grade[i]
                }
                form2 = forms.SaveSubjectResult(data = data)
                if form2.is_valid():
                    form2.save()
                else:
                    resp['msg'] = 'Result Detail has failed to save.'
                    for field in form2:
                        for error in field.errors:
                            resp['msg'] += str(f"<br/> [{field.name}] "+error)
                    has_error = True
                    break
                i +=1
            if has_error == False:
                resp['status'] = 'success'
                messages.success(request, "Result Detail has been saved successfully.")
            else:
                if is_new:
                    models.Result.objects.get(id = post['id']).delete()
        else:
            resp['msg'] = 'Result Detail has failed to save.'
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(f"<br/> [{field.name}] "+error)
    return HttpResponse(json.dumps(resp),content_type="application/json")    

@login_required
def delete_result(request):
    resp = { 'status':'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = 'Request has been sent without data.'
    else:
        post = request.POST
        try:
            models.Result.objects.get(id = post['id']).delete()
            resp['status'] = 'success'
            messages.success(request, "Result Detail has been deleted successfully.")
        except:
            resp['msg'] = 'result Detail has failed to delete.'

    return HttpResponse(json.dumps(resp),content_type="application/json")


def select_student(request):
    context['page'] = 'Select Student'
    context['page_title'] = 'Select Student'
    students = models.Student.objects.filter(status = 1).all()
    context['students'] = students

    return render(request, 'select_student_results.html', context)

def list_student_result(request, pk=None):
    if pk is None:
        messages.error(request, "Invalid Student ID")
        return redirect('login')
    else:
        student = models.Student.objects.get(id = pk)
        results = models.Result.objects.filter(student = student)
        context['student'] = student
        context['results'] = results
        context['page_title'] = str(student) + "'s Results"
        context['has_navigation'] = False
        context['has_sidebar'] = False

    return render(request, 'list_results.html', context)