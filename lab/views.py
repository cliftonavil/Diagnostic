from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings

from lab.forms import ReportForm, CreateTest, CreateAppointment
from .render import Render

from .filters import UserFilter
from .models import Appointment, Testdata, Branch, Employees, TestTaken
from .models import Test
from .import forms
import datetime






def todays_appointments(request):
    # ------- Todays Appointments --------
    todays = Appointment.objects.all().filter(Date=datetime.date.today(),Addedby=request.user)
    path = 'todays_appointments.html'
    return render(request, path, {'todays': todays})


def all_appointments(request):
    # ------- Past Appointments --------
    user_list = Appointment.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    path = 'search_list.html'
    return render(request, path, {'filter': user_filter})

def search(request):
    # ------- Filter  --------
    user_list = Appointment.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    path = 'search_list.html'
    return render(request, path, {'filter': user_filter})

@login_required(login_url='/accounts/login/')
def dashboard(request):
    # ------- Dashboard --------
    test_count = Test.objects.all().filter(availablity_status='available').count()
    #for Admin
    if request.user.is_superuser:
        try:
            todays_count = len(Appointment.objects.all().filter(Date=datetime.date.today(), Addedby=request.user.username))
            rates_list = []
            revenue = TestTaken.objects.all().filter(Today=datetime.date.today())
            # person_count = TestTaken.objects.filter(Today=datetime.date.today()).distinct().count()
            total_test_done = TestTaken.objects.filter(Today=datetime.date.today()).count()
            for i in revenue:
                rates_list.append(int(i.test_id.Rate))
            admin_revenue=sum(rates_list)
        except:
            admin_revenue = '0'
            todays_count = '0'

            person_count='0'
            total_test_done = '0'
        path = 'dashboard.html'
        return render(request, path,
                      {'todays_count': todays_count, 'test_count': test_count, 'admin_revenue': admin_revenue,
                       'total_test_done':total_test_done})
    else:
        #for Other User/Branch
        test_count = len(Test.objects.all().filter(availablity_status='available'))
        print(test_count)
        todays_count = len(Appointment.objects.all().filter(Date=datetime.date.today(), Addedby=request.user.username))
        revenue = TestTaken.objects.all().filter(Username=request.user,Today=datetime.date.today())
        total_test_done = TestTaken.objects.filter(Username=request.user,Today=datetime.date.today()).count()
        person_count = TestTaken.objects.filter(Today=datetime.date.today(),
                                                        Username=request.user).distinct().count()
        rates_list = []
        for i in revenue:
            rates_list.append(int(i.test_id.Rate))
            print(rates_list)
        other_user = sum(rates_list)
        path = 'dashboard.html'
        return render(request, path, {'todays_count': todays_count, 'test_count':test_count,
                                      'other_user':other_user, 'total_test_done':total_test_done,
                                      'person_count':person_count})


def testlist(request):
    # ------- All Test  --------
    data = Test.objects.all()
    context = {'data': data}
    path = 'test_list.html'
    return render(request, path, context)

def appointment_details(request, id):
    # -------  View All Appointment Details  --------
    # app_details = Appointment.objects.get(app_code=app_code)
    app = Appointment.objects.get(id=id)
    testtakenrecord = app.app_code
    check_done = TestTaken.objects.all().filter(app_code=testtakenrecord)
    count = TestTaken.objects.all().filter(app_code=testtakenrecord).count()
    testdata = Test.objects.all()
    path = 'detailed_appointment.html'
    return render(request, path, {'app':app, 'check_done':check_done, 'count':count, 'testdata': testdata })

def todaysappointment_details(request, id):
    #Todays Appointment
    app = Appointment.objects.get(id=id)
    testtakenrecord = app.app_code
    testdata = Test.objects.all()
    check_done = TestTaken.objects.all().filter(app_code=testtakenrecord)
    count = TestTaken.objects.all().filter(app_code=testtakenrecord).count()
    path = 'detailed_appointment_today.html'
    return render(request, path, {'app': app, 'testdata': testdata, 'check_done': check_done,'count':count })


def test_details(request,test_code):
    # -------  View Test Details  --------
    test_details = Test.objects.get(Code=test_code)
    path = 'detailed_test.html'
    return render(request, path, {'test_details': test_details})


def alltestdata(request):
    if request.method == 'POST':
        print('fff')
        app_codes = request.POST.getlist('app_code')
        results = request.POST.getlist('name')
        test_lists = request.POST.getlist('test_list')
        remarks = request.POST.getlist('Remarks')
        for code, result, test_list, remark in zip(app_codes, results, test_lists, remarks):
            test_obj = Test.objects.get(id=test_list)
            record = TestTaken(app_code=code, Username=request.user.username, ResultValue=result,test_id=test_obj,Remarks=remark)
            record.save()
    return render(request, "detailed_appointment.html")


def appointment_create(request):
    #Create Test
    form = forms.CreateAppointment(request.POST or None)
    if form.is_valid():
        print(request.user)
        instance = form.save(commit=False)
        instance.Addedby = request.user
        instance.save()
        form = CreateAppointment()
        return redirect('lab:Dashboard')
    else:
        context={'form':form}
        path = 'appointment_create.html'
    return render(request, path, context)


# def appointment_create(request):
#     #CreateAppointment
#     if request.method == 'POST':
#         form = forms.CreateAppointment(request.POST)
#
#
#         name = form['Name'].value()
#         Date = form['Date'].value()
#         emailto = form['Email'].value()
#
#
#         if form.is_valid():
#             #save article to db
#             instance = form.save(commit=False)
#
#
#             # subject = 'Your Appointment Has been Fixed'
#             # message = ' Dear '+ name +',Your Appointment Time has been Fixed on '+ Date +' at '+ Time +'' \
#             #           '.If any Enquiry Please Contact +919143702167.' \
#             #                                                'Have A Nice Day '
#             # email_from = settings.EMAIL_HOST_USER
#             # recipient_list = [emailto]
#             # send_mail(subject, message, email_from, recipient_list)
#
#
#             instance.Addedby = request.user
#             instance.save()
#         return redirect('lab:Dashboard')
#     else:
#         form = forms.CreateAppointment()
#         path = 'appointment_create.html'
#     return render(request, path, {'form': form})

def create_test(request):
    #Create Test
    form = forms.CreateTest(request.POST or None)
    if form.is_valid():
        form.save()
        form = CreateTest()
        return redirect('lab:Dashboard')
    else:
        context={'form':form}
    return render(request, 'create_new_test.html', context)

def CreateBranch(request):
    #CreateBranch
    if request.method == 'POST':
        form = forms.CreateBranch(request.POST or None)
        if form.is_valid():
            #save article to db
            instance = form.save()
            # instance.author = request.user
            instance.save()
            print('sucesss')
        return redirect('lab:Branch')
    else:
        form = forms.CreateBranch()
        path = 'Create_Branch.html'
    return render(request, path, {'form': form})


def delete_test(request,id):
    testdelete = Test.objects.get(id=id)
    testdelete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TestUpdateForm(ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'Code', 'Referance', 'Unit', 'availablity_status', 'Rate']


def update_test(request, id):
    test = get_object_or_404(Test, id=id)
    form = TestUpdateForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('lab:TestList')
    path='test_update_form.html'
    return render(request, path, {'form': form})


def branch_view(request):
    #Branch main Page
    branch_list = Branch.objects.all()
    path = 'branch_view.html'
    return render(request, path, {'branch_list':branch_list})


def view_branch_detail(request, id):
    branch_details = Branch.objects.get(id=id)
    path = 'branch_details.html'
    return render(request, path, {'branch_details': branch_details})

class BranchUpdateForm(ModelForm):
    class Meta:
        model = Branch
        fields = [ 'branch_name','availablity_status', 'State', 'City',
                   'location', 'Address', 'Phone', 'Email']

def update_branch(request, id):
    test = get_object_or_404(Branch, id=id)
    form = BranchUpdateForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('lab:Branch')
    path = 'branch_update_form.html'
    return render(request, path, {'form': form})

def delete_branch(request, id):
    Branchdelete = Branch.objects.get(id=id)
    Branchdelete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def listallemployee(request):
    listallemployee = Employees.objects.all()
    path = 'view_all_employee.html'
    return render(request, path, {'listallemployee': listallemployee})

def delete_employee(request, id):
    employeedelete = Employees.objects.get(id=id)
    employeedelete.delete()
    return redirect('lab:Listallemployees')

class EmplloyeeUpdateForm(ModelForm):
    class Meta:
        model = Employees
        fields = ['emp_name', 'DOB', 'Designation', 'Joindate',
                  'Mobile', 'emp_branchcode']

def update_employee(request, id):
    test = get_object_or_404(Employees, id=id)
    form = EmplloyeeUpdateForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('lab:Listallemployees')
    path = 'employee_update_form.html'
    return render(request, path, {'form': form})

def create_employee(request):
    #CreateEmployee
    if request.method == 'POST':
        form = forms.EmployeesAdd(request.POST)
        if form.is_valid():
            #save article to db
            instance = form.save()
            # instance.author = request.user
            instance.save()
        return redirect('lab:Listallemployees')
    else:
        form = forms.EmployeesAdd()
        path = 'employee_create_form.html'
    return render(request, path, {'form': form})


def view_detail_employee(request,id):
    employee_details = Employees.objects.get(id=id)
    path = 'employee_in_details.html'
    return render(request, path, {'employee_details': employee_details})



def AdminPrint(request):
    #Generate PDF report for Admin
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            fromformdate = form['fromdate'].value()
            toformdate = form['todate'].value()
            #fromdate
            x=fromformdate.split('-')
            fromyear=int(x[0])
            frommonth=int(x[1])
            fromdate=int(x[2])
            #todate
            y = toformdate.split('-')
            toyear = int(y[0])
            tomonth = int(y[1])
            todate = int(y[2])
            sales = TestTaken.objects.filter(Today__gte=datetime.date(fromyear, frommonth, fromdate),
                                             Today__lte=datetime.date(toyear, tomonth, todate))
            amountlist=[]
            for i in sales:
                amountlist.append(int(i.test_id.Rate))
            totalamount = sum(amountlist)
            username = request.user.username
            params = {
                'sales': sales,
                'fromformdate':fromformdate,
                'toformdate':toformdate,
                'username':username,
                'totalamount':totalamount,
                'now':datetime.datetime.now(),
            }
            return Render.render('Sales_Report_pdf.html', params)
    else:
        form = ReportForm()
        return render(request, 'Admin_Report.html', {'form': form})

def UserPrint(request):
    #Generate PDF report for User
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            fromformdate = form['fromdate'].value()
            toformdate = form['todate'].value()
            #fromdate
            x=fromformdate.split('-')
            fromyear=int(x[0])
            frommonth=int(x[1])
            fromdate=int(x[2])
            #todate
            y = toformdate.split('-')
            toyear = int(y[0])
            tomonth = int(y[1])
            todate = int(y[2])
            sales = TestTaken.objects.filter(Today__gte=datetime.date(fromyear, frommonth, fromdate),
                                             Today__lte=datetime.date(toyear, tomonth, todate),
                                             Username=request.user.username)
            amountlist=[]
            for i in sales:
                amountlist.append(int(i.test_id.Rate))
            totalamount = sum(amountlist)
            params = {
                'sales': sales,
                'fromformdate':fromformdate,
                'toformdate':toformdate,
                'username':request.user.username,
                'totalamount':totalamount,
                'now': datetime.datetime.now(),
            }
            return Render.render('Sales_Report_pdf.html', params)
    else:
        form = ReportForm()
        return render(request, 'User_Report.html', {'form': form})


def visualization(request):
    path='visualization.html'
    return render(request, path, {})

def TestReports(request,string):
    # Generate pdf Medical Reports
    AppointmentData = Appointment.objects.get(app_code=string)
    TestRecords = TestTaken.objects.filter(app_code=string)
    amountlist = []
    for i in TestRecords:
        amountlist.append(int(i.test_id.Rate))
    totalamount = sum(amountlist)
    param={
        'AppointmentData':AppointmentData,
        'TestRecords':TestRecords,
        'username': request.user.username,
        'now': datetime.datetime.now(),
        'totalamount':totalamount,
    }
    return Render.render('TestReport_PDF.html', param)

def Users(request):
    users = User.objects.all()
    path = 'users.html'
    return render(request, path, {'users': users})
