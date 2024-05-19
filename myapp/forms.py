# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'email', 'password1', 'password2']
