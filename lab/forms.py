from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from lab.models import Branch
from .import models


class CreateAppointment(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['Name', 'Age', 'Date','Email']

        widgets = {
            'Name': forms.TextInput(attrs={ 'size': 15,'placeholder': 'Name'}),
            'Age': forms.NumberInput(attrs={'size': 2,'placeholder': 'Age'}),
            'Date': forms.DateInput(attrs={'placeholder': 'Date'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }


class CreateTest(forms.ModelForm):
    class Meta:
        model = models.Test
        fields = ['test_name', 'Code', 'Referance', 'Unit',
                  'availablity_status','Rate']
        widgets = {
            'test_name': forms.TextInput(attrs={'size': 15, 'placeholder': 'Test Name'}),
            'Code': forms.TextInput(attrs={'size': 8, 'placeholder': 'Test Code'}),
            'Referance': forms.TextInput(attrs={'placeholder': 'Referance Value'}),
            'Unit': forms.TextInput(attrs={'placeholder': 'Unit'}),
            'Rate': forms.NumberInput(attrs={'placeholder': 'Rate'}),
        }

class CreateBranch(forms.ModelForm):
    class Meta:
        model = models.Branch
        fields = ['branch_name','availablity_status','State','City','location','Address','Phone',
                  'Email']
        widgets = {
            'branch_name': forms.TextInput(attrs={'size': 15, 'placeholder': 'Branch Code'}),
            'State': forms.TextInput(attrs={'size': 15, 'placeholder': 'State'}),
            'City': forms.TextInput(attrs={'size': 15, 'placeholder': 'City'}),
            'location': forms.TextInput(attrs={'size': 15, 'placeholder': 'Location'}),
            'Address': forms.TextInput(attrs={'size': 15, 'placeholder': 'Address'}),
            'Phone': forms.TextInput(attrs={'size': 15, 'placeholder': 'Phone'}),
            'Email': forms.TextInput(attrs={'size': 15, 'placeholder': 'Email'}),
        }

class EmployeesAdd(forms.ModelForm):
    class Meta:
        model = models.Employees
        fields = ['emp_name','DOB','Designation','Joindate','Mobile','emp_branchcode']
        widgets = {
            'emp_name': forms.TextInput(attrs={'size': 15, 'placeholder': 'Name'}),
            'DOB': forms.DateInput(attrs={'size': 15, 'placeholder': 'DOB'}),
            'Designation': forms.TextInput(attrs={'size': 15, 'placeholder': 'Designation'}),
            'Joindate': forms.DateInput(attrs={'size': 15, 'placeholder': 'Join date'}),
            'Mobile': forms.NumberInput(attrs={'size': 15, 'placeholder': 'Mobile'}),
        }

class Createtestresult(forms.ModelForm):
    class Meta:
        model = models.TestTaken
        fields = ['ResultValue']

class ReportForm(forms.Form):
    fromdate = forms.CharField(max_length=30,required=True, label='From Date')
    todate = forms.CharField(max_length=30,required=True, label='To Date')




