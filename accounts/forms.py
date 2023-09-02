##################
# django imports #
##################
from django import forms

##########################################
#  import modules from current directory #
##########################################
from . models import CustomUser, UserProfile
from . validators import allow_only_images_validator

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


class UserProfileForm(forms.ModelForm):

    #####################
    #  defined fields   #
    #####################
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))

    # inorder for <label class="text-danger">{{ profile_form.profile_picture.errors }}</label> to work
    # we need to change the FileField to ImageField
    # FileField for using 'allow_only_images_validator'
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    # set both  latitude and longitude to 'readonly'
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    #####################
    # defined functions #
    #####################
    
    # create __init__ function to set both  latitude and longitude to 'readonly'
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
