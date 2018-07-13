from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from lab import forms
from lab.filters import UserFilter
from lab.models import Appointment
from lab.models import Test
from .import forms
import datetime

#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

def upcomeing_appointments(request):
    # ------- All Appointments --------
    upcomeing = Appointment.objects.all().filter(Date__gte=datetime.date.today() + datetime.timedelta(days=1))
    path = 'upcomeing_appointments.html'
    return render(request, path, {'upcomeing': upcomeing})


def todays_appointments(request):
    # ------- Todays Appointments --------
    todays = Appointment.objects.all().filter(Date=datetime.date.today())
    path = 'todays_appointments.html'
    return render(request, path, {'todays': todays})


def all_appointments(request):
    # ------- Past Appointments --------
    all = Appointment.objects.all()
    path ='all_appointments.html'
    return render(request, path, {'all': all})


def dashboard(request):
    # ------- Dashboard --------
    todays_count = len(Appointment.objects.all().filter(Date=datetime.date.today()))
    test_count = len(Test.objects.all().filter(availablity_status='available'))
    path = 'dashboard.html'
    print('Username-----',request.user)
    return render(request, path, {'todays_count': todays_count, 'test_count':test_count})


def testlist(request):
    # ------- All Test  --------
    data = Test.objects.all()
    context = {'data': data}
    path = 'test_list.html'
    return render(request, path, context)


def search(request):
    # ------- Filter  --------
    user_list = Appointment.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    path = 'search_list.html'
    return render(request, path, {'filter': user_filter})


def appointment_details(request,app_code):
    # -------  View Appointment Details  --------
    app_details = Appointment.objects.get(app_code=app_code)
    test_name = Test.objects.all().order_by('Name')
    path = 'detailed_appointment.html'
    return render(request, path, {'app_details': app_details, 'test_name': test_name})


def test_details(request,test_code):
    # -------  View Test Details  --------
    test_details = Test.objects.get(Code=test_code)
    print(test_details)
    path = 'detailed_test.html'
    return render(request, path, {'test_details': test_details})

# def home(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         print('cxxxxxxxxxxx',form)
#         if form.is_valid():
#             pass  # does nothing, just trigger the validation
#     else:
#         form = ContactForm()
#     return render(request, 'home.html', {'form': form})



def book_delete(request, id):
    book= Test.objects.get(id=id)
    book.delete()
    path = 'detailed_test.html'
    return render(request, path, {'test_details': test_details})


def appointment_create(request):
    #CreateAppointment
    if request.method == 'POST':
        form = forms.CreateAppointment(request.POST)
        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)
            # instance.author = request.user
            instance.save()
            print('ccccc       Sucess ',form)
        return redirect('lab:Dashboard')
    else:
        form = forms.CreateAppointment()
        path = 'appointment_create.html'
    return render(request, path, {'form': form})
