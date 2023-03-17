from django import forms

from .models import *

class Article_form(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={'required':True,'autofocus':True,'placeholder':"Write title of your story.",'style':'font-size:24px; height:60px; font-weight:600; padding-top:10px; border:1px solid rgb(0,0,0,0.1);'}))
    
    class Meta:
        model = Articles
        fields = ('title','image','content')