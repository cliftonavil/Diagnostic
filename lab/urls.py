from django.urls import path, re_path
from . import views

app_name = 'lab'

urlpatterns = [
    path('todays_appointments', views.todays_appointments, name='Todays Appointments'),
    path('upcomeing_appointments', views.upcomeing_appointments, name='Upcomeings Appointments'),
    path('past_appointments', views.past_appointments, name='Past Appointments'),
    path('dashboard', views.dashboard, name='Dashboard'),
    path('Testlist', views.testlist, name='Test List'),
    path('', views.dashboard, name='Dashboard'),
    path('search', views.search, name='search'),
    re_path(r'^(?P<app_code>\w+)/$', views.appointment_details, name="detail"),
]