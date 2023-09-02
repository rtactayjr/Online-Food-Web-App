##################
# django imports #
##################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


##########################################
#  import modules from current directory #
##########################################
from . forms import MerchantForm
from . models import Merchant

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_merchant


##########################
# Create your views here.#
##########################

@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def merchantProfile(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    merchant = get_object_or_404(Merchant, user=request.user)

    if request.method == 'POST':

        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        merchant_form = MerchantForm(request.POST, request.FILES, instance=merchant)

        if profile_form.is_valid() and merchant_form.is_valid():

            profile_form.save()
            merchant_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('merchantProfile')
        
        else:
            print(profile_form.errors)
            print(merchant_form.errors)

    else:
        profile_form = UserProfileForm(instance = profile)
        merchant_form = MerchantForm(instance= merchant)

    context = {
        'profile_form': profile_form,
        'merchant_form': merchant_form,
        'profile': profile,
        'merchant': merchant,
    }

    return render(request, 'merchants/merchant_profile.html', context)
