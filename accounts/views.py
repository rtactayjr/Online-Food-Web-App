##################
# django imports #
##################
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

##########################################
#  import modules from current directory #
##########################################
from . forms import CustomUserForm
from . models import CustomUser, UserProfile

from merchant.forms import MerchantForm


#############################
# defined functions - views #
#############################

# View function handles the registration of a user.
def registerCustomer(request):

    # Check if the request method is POST
    if request.method == 'POST':

        # This initializes a CustomUserForm instance using the data from the submitted POST request
        form = CustomUserForm(request.POST)

        # Check if the form is valid
        if form.is_valid():

            # Retrieve the cleaned data from the form.password field
            password = form.cleaned_data['password']

            # Prevents the instance from being saved to the DB.
            user = form.save(commit=False)

            # Set the role to 'Customer'
            user.role = CustomUser.CUSTOMER

            # One-way hashing algorithm to securely hash the password before storing it.
            user.set_password(password)

            # Save the user instance to DB and redirect user to the same page.
            form.save()

            # Add message, 'success' can be changed - check bootstrap documentation
            messages.success(request, 'Your account has been successfully registered! Thank you!')

            return redirect(registerCustomer)
        
            '''
            # Create the user using create_user method from 'CustomUserManager'

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = CustomUser.object.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = CustomUser.CUSTOMER 
            user.save()
            '''
            
        # Adding this condition for debugging purposes
        else:
            print('invalid form')
            print(form.errors)
        
    # Return the user to the empty instance of form if method is not 'POST'
    else:
        form = CustomUserForm()
    

    # Dictionary that stores form instance and renders the template passing the context.
    context = {
        'form': form,
    }

    return render(request, 'accounts/registerCustomer.html', context)

# View function handles the registration of a Merchant
def registerMerchant(request):

    if request.method == 'POST':
        # store the data and create the user
        form = CustomUserForm(request.POST)
        merchant_form = MerchantForm(request.POST, request.FILES)

        if form.is_valid() and merchant_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)            
            user.role = CustomUser.MERCHANT
            user.save()

            merchant =  merchant_form.save(commit=False)
            merchant.user = user
            user_profile = UserProfile.objects.get(user=user)
            merchant.user_profile = user_profile
            merchant.save()

            messages.success(request, 'Your account has been registered successfully!')
            return redirect('registerMerchant')

        else:
            print("Invalid Form")
            print(form.errors)
    else:
        form = CustomUserForm(request.POST)
        
    merchant_form = MerchantForm(request.POST, request.FILES)
    
    context = {
        'form': form,
        'merchant_form': merchant_form,
    }

    return render(request, 'accounts/registerMerchant.html', context)
