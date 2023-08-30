##################
# django imports #
##################
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


##########################################
#  import modules from current directory #
##########################################
from . forms import CustomUserForm
from . models import CustomUser, UserProfile
from . utils import detectUser

from merchant.forms import MerchantForm


#############################
# defined functions - views #
#############################

# Restrict the vendor from accessing the customer page
def check_role_merchant(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# View function handles the registration of a user.
def registerCustomer(request):

    # Handle restriction when accessing registration page while user is logged in.
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')

    # Check if the request method is POST
    elif request.method == 'POST':

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
    # Handle restriction when accessing registration page while user is logged in.
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')


    elif request.method == 'POST':
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


def login(request):
    # Handle restriction when accessing login page while user is logged in.
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')

    # Handling the user authentication
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('myAccount')
        else:
            messages.error(request, 'Login failed')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successful')
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user  =  request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def merchantDashboard(request):
    return render(request, 'accounts/merchantDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')