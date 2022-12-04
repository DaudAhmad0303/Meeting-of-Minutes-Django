from django import forms
from userAuthentication.models import user
from django.core.validators import RegexValidator

class signInForm(forms.Form):
    userEmail = forms.EmailField(max_length=100,
                                 widget=forms.EmailInput(attrs={
                                                         'placeholder': 'Email', 'id' : 'userEmail'}),
                                 error_messages={
                                     "required": "Please fill email field to login",
                                     "max_length":"Email should be of less than 100 characters"
                                 }
                                 )
    userPassword = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password',
               "class": "form-control"},),
        error_messages={
            "required": "Please fill email field to login",
    }
    )
    
class signUpForm(forms.ModelForm):
    userEmail = forms.EmailField(required=True,max_length=100,
                                 widget=forms.EmailInput(attrs={
                                                         'placeholder': 'Email', id:"userEmail"}),
                                 error_messages={
                                     "required": "Please fill email field to login",
                                     "max_length":"Email should be of less than 100 characters"
                                 }
                                 )

    class Meta:
        model = user
        fields = ['firstName','lastName','userPassword']
        labels = {
            "userPassword": "Password",
            "firstName": "First Name",
            "lastName": "Last Name",
        }
        error_messages = {
            "userPassword": {
                "required": "Please fill password field to login",
                "min_length":"Password should be of atleast eight characters"
            },
            "firstName": {
                "required": "Please fill user name field to login",
                "max_length":"First Name should be of less than 100 characters"
            },
            "lastName": {
                "required": "Please fill user name field to login",
                "max_length":"Last Name should be of less than 100 characters"
            },
        }

        widgets = {
            'userPassword': forms.PasswordInput(
                attrs={'placeholder': 'Password', id:"userPassword"}
            ),
            'firstName': forms.TextInput(
                attrs={'placeholder': 'First Name', id:"firstName"},
            ),
            'lastName': forms.TextInput(
                attrs={'placeholder': 'Last Name', id:"lastName"},
            ),
        }
    confirmPassword = forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password', "id":"confirmPassword"}),
        error_messages={
        "required": "Please specify confirm password field"
    })
    organizationName= forms.CharField(max_length=100,required=False,widget=forms.TextInput(
        attrs={'placeholder': 'Organization', id:"organizationName"},),
        error_messages={
                "max_length":"Organization Name should be of less than 100 characters"
        }
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    contactNumber = forms.CharField(required=False,validators=[phone_regex], max_length=17,
                    widget=forms.TextInput(attrs={'placeholder': 'Contact', 
                                                  id:"contactNumber"},),
                    error_messages={
                        "max_length":"Contact Number should be of less than 17 characters"
                    }
                    )