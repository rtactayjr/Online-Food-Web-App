##################
# django imports #
##################
from django import forms

##########################################
#  import modules from current directory #
##########################################
from . models import Merchant
from accounts.validators import allow_only_images_validator

#####################
# create class here #
#####################

# Define a form class for the Merchant model
class MerchantForm(forms.ModelForm):
    merchant_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    class Meta:
        # Associate this form with the Merchant model
        model = Merchant

        # Specify the fields to include in the form
        fields = ['merchant_name', 'merchant_license']