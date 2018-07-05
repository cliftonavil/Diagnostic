from django.shortcuts import render
from django.http import HttpResponse

from lab.filters import UserFilter
from lab.models import Appointment, Test
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


def past_appointments(request):
    # ------- Past Appointments --------
    past = Appointment.objects.all().filter(Date__lte=datetime.date.today() - datetime.timedelta(days=1))
    path='past_appointments.html'
    return render(request, path, {'past': past})


def dashboard(request):
    # ------- Dashboard --------
    todays_count = len(Appointment.objects.all().filter(Date=datetime.date.today()))
    test_count = len(Test.objects.all().filter(availablity_status='available'))
    path = 'dashboard.html'
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
    path = 'detailed_appointment.html'
    return render(request, path, {'app_details': app_details})


