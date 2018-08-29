from django.urls import path, re_path
from . import views

app_name = 'lab'

urlpatterns = [
    path('todays_appointments', views.todays_appointments, name='TodaysAppointments'),
    path('all_appointments', views.all_appointments, name='AllAppointments'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('Testlist', views.testlist, name='TestList'),
    path('', views.dashboard, name='home'),
    path('search', views.search, name='search'),
    re_path(r'^all_appointments/(?P<id>\w+)/$', views.appointment_details, name="detail"),
    re_path(r'^todays_appointments/(?P<id>\w+)/$', views.todaysappointment_details, name="todaysdetail"),
    path('appointment_create', views.appointment_create, name='CreateAppointment'),
    path('create_test', views.create_test, name='CreateTest'),
    re_path(r'^Testlist/(?P<id>\w+)/$', views.delete_test, name="DeleteTest"),
    re_path(r'^Testlist/Update/(?P<id>\w+)/$', views.update_test, name="DeleteTest"),
    #Branch
    path('Branch', views.branch_view, name='Branch'),
    path('CreateBranch', views.CreateBranch, name='CreateBranch'),
    re_path(r'^Branch/View/(?P<id>\w+)/$', views.view_branch_detail, name="ViewBranch"),
    re_path(r'^Branch/Update/(?P<id>\w+)/$', views.update_branch, name="UpdateBranch"),
    re_path(r'^Branch/Delete/(?P<id>\w+)/$', views.delete_branch, name="DeleteBranch"),
    #adding test data form
    path('alltestdata', views.alltestdata, name='alltestdata'),
    # path('deletetestdata', views.deletetestdata, name='deletetestdata'),
    path('listallemployee', views.listallemployee, name='Listallemployees'),
    re_path(r'^listallemployee/Delete/(?P<id>\w+)/$', views.delete_employee, name="DeleteEmployee"),
    re_path(r'^listallemployee/Update/(?P<id>\w+)/$', views.update_employee, name="UpdateEmployee"),
    re_path(r'^listallemployee/View/(?P<id>\w+)/$', views.view_detail_employee, name="ViewDetailEmployee"),
    path('create_employee', views.create_employee, name='CreateEmployee'),
    path('User_Report', views.UserPrint,name='UserPrint'),
    path('Addmin_Print', views.AdminPrint,name='AdminPrint'),
    path('visualization', views.visualization,name='visualization'),
    re_path(r'^TestReports/(?P<string>\w+)/$', views.TestReports, name="TestReports"),
    path('Users', views.Users,name='Users')



]