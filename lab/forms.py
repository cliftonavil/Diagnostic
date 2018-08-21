from django import forms
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .import models


class CreateAppointment(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['Name', 'Age', 'Date', 'Time', 'Email', 'phone_number']

        widgets = {
            'Name': forms.TextInput(attrs={ 'size': 15,'placeholder': 'Name'}),
            'Age': forms.NumberInput(attrs={'size': 2,'placeholder': 'Age'}),
            'Date': forms.DateInput(attrs={'placeholder': 'Date'}),
            'Time': forms.TimeInput(attrs={'placeholder': 'Time'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'phone_number': forms.TextInput(attrs={'size': 12,'placeholder': 'Mobile Number'})
        }

    # def clean_name(self):
    #     Name = self.cleaned_data['Name']
    #     print('cccccc   cccccc',age)
    #     return  age


class CreateTest(forms.ModelForm):
    class Meta:
        model = models.Test
        fields = ['test_name', 'Code', 'Referance', 'Unit',
                  'availablity_status','Rate','GST']
        widgets = {
            'test_name': forms.TextInput(attrs={'size': 15, 'placeholder': 'Test Name'}),
            'Code': forms.TextInput(attrs={'size': 8, 'placeholder': 'Test Code'}),
            'Referance': forms.TextInput(attrs={'placeholder': 'Referance Value'}),
            'Unit': forms.TextInput(attrs={'placeholder': 'Unit'}),
            'Rate': forms.NumberInput(attrs={'placeholder': 'Rate'}),
            'GST': forms.NumberInput(attrs={'size': 12, 'placeholder': 'GST in %'})
        }

class CreateBranch(forms.ModelForm):
    class Meta:
        model = models.Branch
        fields = ['branch_code']
        widgets = {
            'branch_code': forms.TextInput(attrs={'size': 15, 'placeholder': 'Branch Code'}),
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