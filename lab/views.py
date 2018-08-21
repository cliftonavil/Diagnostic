from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
# from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.conf import settings


from .filters import UserFilter
from .models import Appointment, Testdata, Branch, Employees, TestTaken
from .models import Test
from .import forms
import datetime




def home(request):
    return render(request, 'home.html')

def todays_appointments(request):
    # ------- Todays Appointments --------
    todays = Appointment.objects.all().filter(Date=datetime.date.today())
    path = 'todays_appointments.html'
    return render(request, path, {'todays': todays})


def all_appointments(request):
    # ------- Past Appointments --------
    user_list = Appointment.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    path = 'search_list.html'
    return render(request, path, {'filter': user_filter})

# @login_required(login_url='/account/login/')
def dashboard(request):
    # ------- Dashboard --------
    todays_count = len(Appointment.objects.all().filter(Date=datetime.date.today()))
    test_count = len(Test.objects.all().filter(availablity_status='available'))
    #for Admin
    if request.user.is_superuser:
        rates_list = []
        revenue = TestTaken.objects.all()
        person_count = TestTaken.objects.values('app_code').distinct().count()
        total_test_done = TestTaken.objects.all().count()
        for i in revenue:
            rates_list.append(int(i.test_id.Rate))
        admin_revenue=sum(rates_list)
        path = 'dashboard.html'
        return render(request, path,
                      {'todays_count': todays_count, 'test_count': test_count, 'admin_revenue': admin_revenue,
                       'person_count':person_count,'total_test_done':total_test_done})
    else:
        #for Other User/Branch
        rates_list = []
        revenue = TestTaken.objects.all().filter(Username=request.user.username)
        try:
            total_test_done = TestTaken.objects.get(Username=request.user.username).count()
        except:
            total_test_done="Not Available"
        for i in revenue:
            rates_list.append(int(i.test_id.Rate))
        other_user=sum(rates_list)
        path = 'dashboard.html'
        return render(request, path, {'todays_count': todays_count, 'test_count':test_count,
                                  'other_user':other_user, 'total_test_done':total_test_done})


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


def appointment_details(request, id):
    # -------  View Appointment Details  --------
    # app_details = Appointment.objects.get(app_code=app_code)
    app = Appointment.objects.get(id=id)
    testdata = Test.objects.all()
    check_done = TestTaken.objects.all()
    path = 'detailed_appointment.html'
    return render(request, path, {'app':app, 'testdata':testdata, 'check_done':check_done })


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







#
# def deletetestdata(request):
#     if request.method == 'POST':
#         record_id = request.POST.getlist('id')
#         print('Backend')
#         for i in record_id:
#             print('Backend',i)
#             print('ccccccccccccccccccccccc')
#             delete_record = TestTaken.objects.get(id=int(i))
#             delete_record.delete()






def appointment_create(request):
    #CreateAppointment
    if request.method == 'POST':
        form = forms.CreateAppointment(request.POST)


        name = form['Name'].value()
        Date = form['Date'].value()
        Time = form['Time'].value()
        emailto = form['Email'].value()


        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)


            # subject = 'Your Appointment Has been Fixed'
            # message = ' Dear '+ name +',Your Appointment Time has been Fixed on '+ Date +' at '+ Time +'' \
            #           '.If any Enquiry Please Contact +919143702167.' \
            #                                                'Have A Nice Day '
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [emailto]
            # send_mail(subject, message, email_from, recipient_list)


            # instance.author = request.user
            instance.save()
        return redirect('lab:Dashboard')
    else:
        form = forms.CreateAppointment()
        path = 'appointment_create.html'
    return render(request, path, {'form': form})


def create_test(request):
    #CreateAppointment
    if request.method == 'POST':
        form = forms.CreateTest(request.POST)
        if form.is_valid():
            #save article to db
            instance = form.save()
            # instance.author = request.user
            instance.save()
        return redirect('lab:Dashboard')
    else:
        form = forms.CreateTest()
        path = 'create_new_test.html'
    return render(request, path, {'form': form})

def create_banch(request):
    #CreateBranch
    if request.method == 'POST':
        form = forms.CreateBranch(request.POST)
        if form.is_valid():
            #save article to db
            instance = form.save()
            # instance.author = request.user
            instance.save()
        return redirect('lab:Dashboard')
    else:
        form = forms.CreateBranch()
        path = 'banch_view.html'
    return render(request, path, {'form': form})


def delete_test(request,id):
    testdelete = Test.objects.get(id=id)
    testdelete.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TestUpdateForm(ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'Code', 'Referance', 'Unit', 'availablity_status', 'Rate','GST']


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
        fields = [ 'availablity_status', 'State', 'City',
                   'location', 'Address', 'Incharge', 'Phone', 'Email']

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
    return render(request, path, {'branch_details': employee_details})



# from django.core.mail import EmailMessage
# from django.core.mail.backends.smtp import EmailBackend
#
#
# config = Configuration.objects.get(**lookup_kwargs)
#
# backend = EmailBackend(host=config.host, port=congig.port, username=config.username,
#                        password=config.password, use_tls=config.use_tls, fail_silently=config.fail_silently)

# def pdf_view(request):
#     # Create the HttpResponse object with the appropriate PDF headers.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
#     p = canvas.Canvas(response)
#     p.drawString(100, 100, 'hiii')
#     p.showPage()
#     p.save()
#     return response

# 4147201115