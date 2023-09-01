##################
# django imports #
##################
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode


##########################################
#  import modules from current directory #
##########################################
from . forms import CustomUserForm
from . models import CustomUser, UserProfile
from . utils import detectUser, send_verification_email

from merchant.forms import MerchantForm


#############################
# defined functions - views #
#############################


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = CustomUser.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


# This function is used to activate a user's account based on a verification link they've clicked
def activate(request, uidb64, token):
    try:
        # This line decodes the URL-safe encoded user's primary key into a string format.
        uid = urlsafe_base64_decode(uidb64).decode()

        # sing the primary key, the function tries to retrieve the corresponding user from the database
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    # Activate the user by setting the is_active status to True
    # This checks whether the token is valid for the given user.
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')


""" Handles Registration for Customer and Merchants """
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

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            # Add message, 'success' can be changed - check bootstrap documentation
            # connected to 'alerts.html'
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
        messages.warning(request, 'You are already logged in') # connected to 'alerts.html'
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

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered successfully!') # connected to 'alerts.html'
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


""" Handles Login and Logout - authentication """

def login(request):
    # Handle restriction when accessing login page while user is logged in.
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in') # connected to 'alerts.html'
        return redirect('myAccount')

    # Handling the user authentication
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        # Check if the user is exist, otherwise throw an error and stay in login page.
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!') # connected to 'alerts.html'
            return redirect('myAccount')
        else:
            messages.error(request, 'Login failed') # connected to 'alerts.html'
            return redirect('login')

    return render(request, 'accounts/login.html')

# Handles the logout of the account
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successful') # connected to 'alerts.html'
    return redirect('login')


""" Handles Role Detection and Url Redirection """

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

# Handles the user detection of user Role
# Function 'detectUser' is from utils.py
@login_required(login_url='login')
def myAccount(request):
    user  =  request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# redirect Merchant to Merchant Dashboard
@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def merchantDashboard(request):
    return render(request, 'accounts/merchantDashboard.html')

# redirect to Customer Dashboard
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')