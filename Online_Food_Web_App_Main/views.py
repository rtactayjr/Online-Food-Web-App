##################
# django imports #
##################
from django.shortcuts import render
from django.http import HttpResponse

from merchant.models import Merchant
#####################
# defined functions #
#####################
def home(request):
    merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)[:8]
  
    context = {
        'merchants':merchants,
    }
 
    return render(request, 'home.html', context)