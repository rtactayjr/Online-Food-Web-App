##################
# django imports #
##################
from django.shortcuts import render

##########################################
#  import modules from current directory #
##########################################
from merchant.models import Merchant

#############################
# defined functions - views #
#############################

def marketplace(request):
    merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)
    merchant_count = merchants.count()

    context = {
        'merchants': merchants,
        'merchant_count': merchant_count,
    }

    return render(request, 'marketplace/product_listings.html', context)