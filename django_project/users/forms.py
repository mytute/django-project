from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from .models import Profile  

# class inherite by "UserCreationForm"
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() # (required=False) if optional 

    
    class Meta:
        model = User # validate with "User" model and save on "User" table   
        fields = ['username', 'email', 'password1', 'password2'] #  define display order of fields 

# for update "username" and "email"
class UserUpdateForm(forms.ModelForm):
  email = forms.EmailField() # additional field that we added  

  class Meta:
    model = User
    fields = ['username', 'email']

# for update "image" filed
class ProfileUpdateForm(forms.ModelForm):

  class Meta:
    model = Profile 
    fields = ['image']

