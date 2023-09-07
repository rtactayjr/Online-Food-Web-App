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
    # Retrieve a list of approved and active merchants (up to 8) for display on the home page
    merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)[:8]
  
    # Create a context dictionary to pass data to the template
    context = {
        'merchants': merchants,  # Provide the list of merchants to the template
    }
 
    # Render the 'home.html' template with the provided context
    return render(request, 'home.html', context)
