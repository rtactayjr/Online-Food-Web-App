"""
In Django, context processors are functions that allow you to add data to the context of every template rendered for a request. 
This means you can make certain data available globally to all templates, without having to explicitly pass it from each view function.

Purpose:
Global Data: Context processors are used to provide global data that you want to be available in all templates across your Django project. 
This data can be dynamic, such as user information, or static, like configuration settings.

Avoid Repetition: They help you avoid repeating data in every view function. 
Instead of manually passing the same data to the template context in every view, you can use a context processor to include it automatically.

Example Use Cases:
User Authentication: You can use a context processor to make the current user's information (if authenticated) available in every template, allowing you to display their username, profile picture, or authentication status.

Site-Wide Configuration: You can provide configuration settings, like the site's name, logo URL, or contact information, to all templates without 
needing to pass them explicitly in every view.

Registering Context Processors: 
To use a context processor, you need to register it in your project's settings. 
Context processors are defined as callables (functions or classes with a __call__ method). 
You typically add them to the context_processors list in the TEMPLATES setting of your project's settings.py file.

"""

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