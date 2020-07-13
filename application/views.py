from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import json
# Create your views here.


def index(request):
    context = {}

    all_depts = department.objects.all()
    context['departments'] = all_depts

    all_my_doctors = doctors.objects.all()
    context['doctors'] = all_my_doctors

    if request.user.is_authenticated:
        requested_doctors = appointment.objects.filter(sender_patient=request.user).values_list('to_doctor', flat=True)
    
        context['requested_doctors'] = requested_doctors


    return render(request, 'index.html', context)

def send_request(request):
    if request.method == "GET" and request.is_ajax():
        doctor_id = request.GET['doctor_id']
        doctor_id = int(doctor_id)

        thisDoct = doctors.objects.get(id=doctor_id)
        dept = thisDoct.profession


        first_check = len(appointment.objects.filter(sender_patient=request.user, status=0))
        
        if first_check < 3:
            
            second_check = len(appointment.objects.filter(sender_patient=request.user, status=0, depart=dept))

            if second_check < 1:

                new_appoint = appointment(sender_patient=request.user, to_doctor=thisDoct, depart=dept)
                new_appoint.save()
                return HttpResponse(json.dumps({'message': "Your request has been sent", 'status':1}), content_type="application/json")

            else:
                new_fake = fakes(request.user)
                return HttpResponse(json.dumps({'message': "Sorry You have sent request to the same department.", 'status':0}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({'message': "You can't send more request to the doctos", 'status':0}), content_type="application/json")






def per_doct(request, id):
    doct_id = id

    context = {}

    this_doct = doctors.objects.get(id=doct_id)
    context['doctor'] = this_doct
    return render(request, "doct.html", context)


def myProfile(request):

    if request.method == 'POST' and 'AP_ID' in request.POST and 'DATE' in request.POST:
        AP_ID = int(request.POST['AP_ID'])
        DATE = request.POST['DATE']
        TIME = request.POST['TIME']

        appoint = appointment.objects.get(id=AP_ID)
        appoint.appointment_date = DATE
        appoint.appointment_time = TIME
        appoint.status = 1
        appoint.save()



    return profile(request, request.user.id)

def reject(request, id):
    appoint = appointment.objects.get(id=id)
    appoint.status = -1
    appoint.save()

    return profile(request, request.user.id)

def completed(request, id):
    appoint = appointment.objects.get(id=id)
    appoint.status = 2
    appoint.save()

    return profile(request, request.user.id)


def profile(request, id):
    context = {}
    if request.user.is_authenticated and request.user.id == id:
        getUser = User.objects.get(id=id)
        

        if doctors.objects.filter(email=getUser.username).exists():
            all_doc = doctors.objects.filter(email=getUser.username)[0]
            context['is_doctor'] = True
            get_whole_info = all_doc
            print(all_doc.hospital)
            context['user_info'] = get_whole_info
            all_appoints = appointment.objects.filter(to_doctor=get_whole_info)
            context['all_appoints'] = all_appoints
        else:
            context['is_doctor'] = False
            all_appoints = appointment.objects.filter(sender_patient=request.user)
            context['all_appoints'] = all_appoints

        return render(request, "profile.html", context)
    else:
        return redirect("index")

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered number already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return redirect("login")
    else:
        return render(request, "login.html")

def all_doctors(request):
    context = {}
    all_my_doctors = doctors.objects.all()
    context['doctors'] = all_my_doctors
    context['title'] = ["All Doctors", ""]

    if request.user.is_authenticated:
        requested_doctors = appointment.objects.filter(sender_patient=request.user).values_list('to_doctor', flat=True)
    
        context['requested_doctors'] = requested_doctors


    return render(request, 'Doctors.html', context)


def logout(request):
    auth.logout(request)
    return redirect("index")

def all_departments(request):
    context = {}
    all_depts = department.objects.all()
    context['departments'] = all_depts
    return render(request, 'Department.html', context)

def per_department(request, name):
    context = {}
    dept = department.objects.get(name=name)
    filtered_doc = doctors.objects.filter(profession=dept.related_profession_name)
    context['title'] = [dept.name, "Departments / "+dept.name]
    context['doctors'] = filtered_doc
    return render(request, 'Doctors.html', context)