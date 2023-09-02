##################
# django imports #
##################
from django import forms

##########################################
#  import modules from current directory #
##########################################
from . models import Merchant

#####################
# create class here #
#####################

# Define a form class for the Merchant model
class MerchantForm(forms.ModelForm):
    class Meta:
        # Associate this form with the Merchant model
        model = Merchant

        # Specify the fields to include in the form
        fields = ['merchant_name', 'merchant_license']