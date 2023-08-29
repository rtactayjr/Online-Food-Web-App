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
class MerchantForm(forms.ModelForm):
     class Meta:
        model = Merchant
        fields = ['merchant_name', 'merchant_license']