from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  

# class inherite by "UserCreationForm"
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # (required=False) if optional 

    
    class Meta:
        model = User # validate with "User" model and save on "User" table   
        fields = ['username', 'email', 'password1', 'password2'] #  define display order of fields 
