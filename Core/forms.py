from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'required':True,'placeholder':"First name",'style':'font-size:14px;'}),label=False)
    last_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'required':True,'placeholder':"Last name",'style':'font-size:14px;'}),label=False)
    email = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'required':True,'placeholder':"Enter Email Id",'style':'font-size:14px;'}),label=False)
    

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2' )