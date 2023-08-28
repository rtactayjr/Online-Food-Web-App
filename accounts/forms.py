##################
# django imports #
##################
from django import forms

##########################################
#  import modules from current directory #
##########################################
from . models import CustomUser

#####################
# create class here #
#####################
"""
Create class to inherit 'ModelForm'. 
By using a ModelForm, you can leverage Django's built-in form handling and validation while closely matching the structure of the underlying model.

added 2 fields for 'password' and 'confirm_password'

class 'Meta' is a way to provide configuration and metadata for classes like models and forms, allowing you to control their behavior and appearance.
""" 
class CustomUserForm(forms.ModelForm):

    #####################
    #  defined fields   #
    #####################
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


    #####################
    # defined functions #
    #####################
    """
    cleaned_data = super(CustomUserForm, self).clean(): This line gets the cleaned data dictionary for all form fields

    password = cleaned_data.get('password'): 
    confirm_password = cleaned_data.get('confirm_password'):
    -- This line retrieves the cleaned data for the "password" field from the cleaned_data dictionary using the .get() method. 

    """
    def clean(self):
        cleaned_data = super(CustomUserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match!')
