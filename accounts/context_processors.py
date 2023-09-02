##################
# django imports #
##################
from urllib.parse import uses_relative
from django.conf import settings

##########################################
#  import modules from current directory #
##########################################
from accounts.models import UserProfile
from merchant.models import Merchant

#############################
# defined functions - views #
#############################


def get_merchant(request):
    try:
        merchant = Merchant.objects.get(user=request.user)
    except:
        merchant = None
    return dict(merchant=merchant)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)



def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}


def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}