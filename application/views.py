from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count
import json
# Create your views here.



def partition(arr,low,high): 
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high].all_ratings    # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than the pivot 
        if   arr[j].all_ratings > pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)



def get_ratings_objects(myList, con):
    temping = []
    if not con:
        for i in myList:
            t = doctor_with_review(i)
            temping.append(t)
    else:
        for i in myList:
            t = doctor_with_review(i)
            if t.all_ratings != 0:
                temping.append(t)

    return temping



def index(request):
    context = {}

    all_depts = department.objects.all()
    context['departments'] = all_depts

    all_my_doctors = doctors.objects.all()

    all_doctors_with_review = get_ratings_objects(all_my_doctors, True)

    quickSort(all_doctors_with_review,0,len(all_doctors_with_review)-1)

    context['rec_doctor'] = all_doctors_with_review

    # context['doctors'] = get_ratings_objects(all_my_doctors, False)

    if request.user.is_authenticated:
        requested_doctors1 = list(appointment.objects.filter(sender_patient=request.user, status=1).values_list('to_doctor', flat=True))
        requested_doctors2 = list(appointment.objects.filter(sender_patient=request.user, status=0).values_list('to_doctor', flat=True))
        requested_doctors = requested_doctors1 + requested_doctors2
        context['requested_doctors'] = requested_doctors


    return render(request, 'index.html', context)


def send_request(request):
    if request.method == "GET" and request.is_ajax():
        doctor_id = request.GET['doctor_id']
        doctor_id = int(doctor_id)

        thisDoct = doctors.objects.get(id=doctor_id)
        dept = thisDoct.profession

        isThisDoctor = doctors.objects.filter(email=request.user.username).exists()

        if isThisDoctor:
            return HttpResponse(json.dumps({'message': "You are a doctor, You can't send appointment request", 'status':0}), content_type="application/json")

        
        else:
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

    if request.method == 'POST':
     
        doctor_id = int(request.POST['doctID'])
        
        review_msg = request.POST['myReview']
        review_stars = request.POST['ratings']
        main_doc = doctors.objects.get(id=doctor_id)
        author = request.user

        new_review = doctor_review(author=author, review_star=review_stars, review_msg=review_msg, doctor=main_doc)
        new_review.save()

        print("review_msg =", review_msg)
        print("review_stars =", review_stars)
        print("main_doc =", main_doc.first_name)
        print("author =", author.first_name)


    doct_id = id

    context = {}

    

    this_doct = doctors.objects.get(id=doct_id)
    context['doctor'] = this_doct
    all_reviews = doctor_review.objects.filter(doctor=this_doct)
    context['reviews'] = all_reviews
    context['review_view'] = True

    if request.user.is_authenticated:
        requested_doctors1 = list(appointment.objects.filter(sender_patient=request.user, status=1).values_list('to_doctor', flat=True))
        requested_doctors2 = list(appointment.objects.filter(sender_patient=request.user, status=0).values_list('to_doctor', flat=True))
        requested_doctors = requested_doctors1 + requested_doctors2
        context['requested_doctors'] = requested_doctors

    return render(request, "profile.html", context)


def myProfile(request):

    if request.method == 'POST' and 'AP_ID' in request.POST and 'DATE' in request.POST:
        AP_ID = int(request.POST['AP_ID'])
        DATE = request.POST['DATE']
        TIME = request.POST['TIME']

        if appointment.objects.filter(appointment_date=DATE, appointment_time=TIME).exists():
            messages.info(request, "Sorry! this date & time is already booked for appointment")
        else:
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

            
            # all_appoints = appointment.objects.filter(to_doctor=get_whole_info)
            # context['all_appoints'] = all_appoints

            if request.method == 'POST' and 'leave_date' in request.POST:
                leave_date = request.POST['leave_date']
                new_leave = doctor_leave(doctor=get_whole_info, leave_date=leave_date)
                new_leave.save()

                # appointment cancellation
                
                if appointment.objects.filter(to_doctor=get_whole_info, appointment_date=leave_date).exists():
                    all_appointments_of_this_date = appointment.objects.filter(to_doctor=get_whole_info, appointment_date=leave_date)

                    for i in all_appointments_of_this_date:
                        i.status = -2
                        i.save()
                
                print('leave_date =', leave_date)

                context['leave_taken'] = doctor_leave.objects.filter(doctor=get_whole_info).exists()

            
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
    context['rec_doctor'] = get_ratings_objects(all_my_doctors, True)
    
    context['title'] = ["All Doctors", ""]

    if request.user.is_authenticated:
        requested_doctors1 = list(appointment.objects.filter(sender_patient=request.user, status=1).values_list('to_doctor', flat=True))
        requested_doctors2 = list(appointment.objects.filter(sender_patient=request.user, status=0).values_list('to_doctor', flat=True))
        requested_doctors = requested_doctors1 + requested_doctors2
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
    context['rec_doctor'] = get_ratings_objects(filtered_doc, False)

    for i in context['rec_doctor']:
        print(i.all_ratings)
        # print(i.first_name)

    if request.user.is_authenticated:
        requested_doctors1 = list(appointment.objects.filter(sender_patient=request.user, status=1).values_list('to_doctor', flat=True))
        requested_doctors2 = list(appointment.objects.filter(sender_patient=request.user, status=0).values_list('to_doctor', flat=True))
        requested_doctors = requested_doctors1 + requested_doctors2
        context['requested_doctors'] = requested_doctors


    return render(request, 'Doctors.html', context)