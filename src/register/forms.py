from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import fields

class RegisterForm(UserCreationForm):
    enroll_no = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'enroll_no', 'password1', 'password2']
        