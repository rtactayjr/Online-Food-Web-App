##################
# django imports #
##################
from django.shortcuts import render

##########################
# Create your views here.#
##########################

def merchantProfile(request):
    return render(request, 'merchants/merchant_profile.html')