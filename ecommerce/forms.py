from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Customer,Contact

class LoginForm(forms.Form):
    username=forms.EmailField(label='Email',required=True)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput,required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-fields'})
        # self.fields['email'].widget.attrs.update({'class': 'form-fields'})
        self.fields['password'].widget.attrs.update({'class': 'form-fields'})
    # email=forms.EmailField(label='Email',max_length=250)


class CreateUserForm(UserCreationForm):
    # email=forms.EmailField(required=True)
    username=forms.EmailField(label='Email',required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-fields'})
        # self.fields['email'].widget.attrs.update({'class': 'form-fields'})
        self.fields['password1'].widget.attrs.update({'class': 'form-fields'})
        self.fields['password2'].widget.attrs.update({'class': 'form-fields'})
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        # teke username as email
        # fields=['username','email','password1','password2']
        
class CustomerForm(ModelForm):
    first_name=forms.CharField(label='First Name',required=True)
    last_name=forms.CharField(label='Last Name',required=True)
    addressline1=forms.CharField(label='AddressLine1',required=True)
    addressline2=forms.CharField(label='AddressLine2',required=True)
    city=forms.CharField(label='City',required=True)
    state=forms.CharField(label='State',required=True)
    country=forms.CharField(label='Country',required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-fields'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-fields'})
        self.fields['addressline1'].widget.attrs.update({'class': 'form-fields'})
        self.fields['addressline2'].widget.attrs.update({'class': 'form-fields'})
        self.fields['city'].widget.attrs.update({'class': 'form-fields'})
        self.fields['state'].widget.attrs.update({'class': 'form-fields'})
        self.fields['country'].widget.attrs.update({'class': 'form-fields'})
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']
        
#not used for now
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-fields','disabled':True})
    class Meta:
        model=User
        # fields='__all__'
        fields=['email']
    
class ContactForm(ModelForm):
    name=forms.CharField(label='Name',required=True)
    email=forms.CharField(label='Email',required=True)
    comment=forms.Textarea()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-fields'})
        self.fields['email'].widget.attrs.update({'class': 'form-fields'})
        self.fields['comment'].widget.attrs.update({'class': 'form-fields'})
    class Meta:
        model=Contact
        fields='__all__'
    
    

