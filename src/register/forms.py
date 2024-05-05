from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    isAdmin = forms.BooleanField(label='Admin?', required=False)

   # class Meta:
     #  model = User
     #  fields = ["isAdmin"]

   # def __init__(self, *args, **kwargs):
      #  super().__init__(*args, **kwargs)
        #self.fields["username"].widget.attrs.update({
           # 'required': 'True',
           # 'name': 'username',
           # 'id': 'username',
           # 'type': 'text',
           # 'class': 'form-input',
          # 'placeholder': 'Username'

      #  })

       # self.fields["isAdmin"].widget.attrs.update({
        #    'required': False,
         #   'name': 'isAdmin',
         #   'id': 'isAdmin',
          #  'type': 'checkbox',
          #  'class': 'form-input',

       # })

       # self.fields["password1"].widget.attrs.update({
          #  'required': 'True',
          #  'name': 'password1',
         #   'id': 'password1',
          #  'type': 'password',
          #  'class': 'form-input',
           # 'placeholder': 'Password'
            
       # })

        #self.fields["password2"].widget.attrs.update({
           # 'required': 'True',
          #  'name': 'password2',
           # 'id': 'password2',
           # 'type': 'password',
           # 'class': 'form-input',
          #  'placeholder': 'Confirm Password'
            
       # })

