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
from django.template.defaultfilters import slugify


##########################################
#  import modules from current directory #
##########################################
from . forms import CustomUserForm
from . models import CustomUser, UserProfile
from . utils import detectUser, send_verification_email

from merchant.forms import MerchantForm
from merchant.models import Merchant
from orders.models import Order




#############################
# defined functions - views #
#############################

""" Handles Reset Password Feature and Validation """
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Get user exact email address
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
    # Try to validate the user by decoding the token and user pk
    try:
        # Decode the URL-safe base64 encoded string 'uidb64' and convert it to a plain string 'uid'
        uid = urlsafe_base64_decode(uidb64).decode()

        # Attempt to retrieve a user object from the database using the decoded 'uid' as the primary key
        user = CustomUser._default_manager.get(pk=uid)

    # Handle exceptions that might occur during the validation process
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        # If an exception occurs, set 'user' to 'None' to indicate validation failure
        user = None

    # Check if the 'user' object is not 'None' and if the provided 'token' is valid
    if user is not None and default_token_generator.check_token(user, token):
        # If both conditions are met, store the 'uid' in the session (for password reset context)
        request.session['uid'] = uid

        # Provide an informational message to the user
        messages.info(request, 'Please reset your password')

        # Redirect the user to the 'reset_password' view
        return redirect('reset_password')
    
    else:
        # If the user is 'None' or the token is invalid, show an error message
        messages.error(request, 'This link has expired!')

        # Redirect the user to the 'myAccount' view
        return redirect('myAccount')


def reset_password(request):
    # Check if the HTTP request method is POST (indicating a form submission)
    if request.method == 'POST':
        # Get the 'password' and 'confirm_password' values from the POST data
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the entered 'password' matches the 'confirm_password'
        if password == confirm_password:
            # Retrieve the 'uid' from the session (set during the password reset link validation)
            pk = request.session.get('uid')
            
            # Retrieve the user associated with the 'uid'
            user = CustomUser.objects.get(pk=pk)

            # Set the user's password to the new password
            user.set_password(password)

            # Activate the user by setting 'is_active' to True
            user.is_active = True

            # Save the user object with the updated password and activation status
            user.save()

            # Provide a success message to the user
            messages.success(request, 'Password reset successful')

            # Redirect the user to the 'login' view
            return redirect('login')
        else:
            # If the entered passwords do not match, show an error message
            messages.error(request, 'Passwords do not match!')

            # Redirect the user back to the 'reset_password' view
            return redirect('reset_password')

    # If the HTTP request method is not POST, render the 'reset_password' template
    return render(request, 'accounts/reset_password.html')



""" Handles Account activation for Merchants/Customers """
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
    
    # Check if the user is already authenticated (logged in)
    if request.user.is_authenticated:

        # If logged in, show a warning message and redirect to 'myAccount'
        messages.warning(request, 'You are already logged in')  # Connected to 'alerts.html'
        return redirect('myAccount')

    # If the HTTP request method is POST (form submission)
    elif request.method == 'POST':
        # Create form instances for 'CustomUserForm' and 'MerchantForm' using POST data
        form = CustomUserForm(request.POST)
        merchant_form = MerchantForm(request.POST, request.FILES)

        # Check if both forms are valid
        if form.is_valid() and merchant_form.is_valid():
            # Extract cleaned data from the 'CustomUserForm'
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create a new user using the extracted data
            user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            
            # Set the user's role to 'MERCHANT'
            user.role = CustomUser.MERCHANT
            user.save()

            # Create a new merchant instance and associate it with the user
            merchant = merchant_form.save(commit=False)
            merchant.user = user

            merchant_name = merchant_form.cleaned_data['merchant_name']
            merchant.merchant_slug = slugify(merchant_name)+'-'+str(user.id)

            # Get the user's profile and associate it with the merchant
            user_profile = UserProfile.objects.get(user=user)
            merchant.user_profile = user_profile
            merchant.save()

            # Send a verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            # Provide a success message to the user
            messages.success(request, 'Your account has been registered successfully')  # Connected to 'alerts.html'
            return redirect('registerMerchant')

        else:
            # If the forms are invalid, print error messages (for debugging) and handle as needed
            print("Invalid Form")
            print(form.errors)

    # If the HTTP request method is not POST, render the registration form
    else:
        # Create form instances for 'CustomUserForm' and 'MerchantForm'
        form = CustomUserForm()
        merchant_form = MerchantForm()

    # Create a context dictionary with form instances
    context = {
        'form': form,
        'merchant_form': merchant_form,
    }

    # Render the 'registerMerchant' template with the context
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

# Check if the user has the 'MERCHANT' role, if not, raise a PermissionDenied exception
def check_role_merchant(user):
    if user.role == CustomUser.MERCHANT:
        return True
    else:
        raise PermissionDenied

# Check if the user has the 'CUSTOMER' role, if not, raise a PermissionDenied exception
def check_role_customer(user):
    if user.role == CustomUser.CUSTOMER:
        return True
    else:
        raise PermissionDenied

# Handles user detection of user Role and redirects accordingly
@login_required(login_url='login')
def myAccount(request):
    # Get the currently logged-in user
    user = request.user

    # Detect the appropriate redirect URL based on the user's role
    redirect_url = detectUser(user)

    # Redirect the user to the determined URL
    return redirect(redirect_url)

# Redirects the merchant to the Merchant Dashboard
@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def merchantDashboard(request):
    # Get the merchant associated with the currently logged-in user
    merchant = Merchant.objects.get(user=request.user)

    context = {
        'merchant': merchant,
    }
    
    # Render the 'merchantDashboard' template with the merchant's context
    return render(request, 'accounts/merchantDashboard.html', context)

# Redirects to the Customer Dashboard
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):

    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
    }

    # Render the 'customerDashboard' template
    return render(request, 'accounts/customerDashboard.html', context)
