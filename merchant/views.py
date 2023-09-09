##################
# django imports #
##################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.http import HttpResponse, JsonResponse

from django.db import IntegrityError


##########################################
#  import modules from current directory #
##########################################
from . forms import MerchantForm, OperatingHourForm
from . models import Merchant, OperatingHour

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_merchant

from menuitems.models import ProductCategory, ProductItem
from menuitems.forms import ProductCategoryForm, ProductItemForm

##########################
# Create your views here.#
##########################

@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def merchantProfile(request):
    # Retrieve the user's profile and merchant objects
    profile = get_object_or_404(UserProfile, user=request.user)
    merchant = get_object_or_404(Merchant, user=request.user)

    # Check if the request method is POST
    if request.method == 'POST':

        # Create instances of profile and merchant forms with POST data
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        merchant_form = MerchantForm(request.POST, request.FILES, instance=merchant)

        # Check if both profile and merchant forms are valid
        if profile_form.is_valid() and merchant_form.is_valid():

            # Save the profile and merchant forms
            profile_form.save()
            merchant_form.save()

            # Display a success message and redirect to the merchantProfile page
            messages.success(request, 'Settings updated.')
            return redirect('merchantProfile')

        else:
            # If forms are not valid, print the form errors for debugging
            print(profile_form.errors)
            print(merchant_form.errors)

    else:
        # If the request method is not POST, create instances of profile and merchant forms
        # without POST data to display them to the user
        profile_form = UserProfileForm(instance=profile)
        merchant_form = MerchantForm(instance=merchant)

    context = {
        'profile_form': profile_form,
        'merchant_form': merchant_form,
        'profile': profile,
        'merchant': merchant,
    }

    # Render the merchant_profile.html template with the context
    return render(request, 'merchants/merchant_profile.html', context)


# Function to get the current logged in Merchant
def get_merchant(request):
    merchant = Merchant.objects.get(user=request.user)
    return merchant

# Ensure that the user is logged in and has the role of a merchant
@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def menu_builder(request):

    # Retrieve the currently logged-in merchant
    merchant = get_merchant(request)

    # Retrieve all product categories owned by the merchant and order them by creation date
    categories = ProductCategory.objects.filter(merchant=merchant).order_by('created_at')

    # Pass the values of 'categories' as context
    context = {
        'categories': categories,
    }

    # Render the 'menu_builder.html' template with the provided context
    return render(request, 'merchants/menu_builder.html', context)


# Ensure that the user is logged in and has the role of a merchant
@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def product_items_by_category(request, pk=None):

    # Retrieve the currently logged-in merchant
    merchant = get_merchant(request)

    # Retrieve the product category matching the provided primary key (pk)
    category = get_object_or_404(ProductCategory, pk=pk)

    # Retrieve all product items owned by the merchant in the specified category
    productitems = ProductItem.objects.filter(merchant=merchant, category=category)

    # Pass the retrieved data as context
    context = {
        'productitems': productitems,
        'category': category,
    }

    # Render the 'productitems_by_category.html' template with the provided context
    return render(request, 'merchants/product_items_by_category.html', context)


# Ensure that the user is logged in and has the role of a merchant
@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def add_product_category(request):

    # Check if the request method is POST
    if request.method == 'POST':

        # Create a ProductCategoryForm instance based on the data received in the POST request
        form = ProductCategoryForm(request.POST)

        # Check if the submitted form is valid
        if form.is_valid():
            
            # Retrieve the category name from the form data
            category_name = form.cleaned_data['category_name']

            # Create a ProductCategory instance but don't save it to the database yet
            category = form.save(commit=False)

            # Set the merchant for the category to the currently logged-in merchant
            category.merchant = get_merchant(request)

            # Save the category to the database
            category.save()

            # Generate a unique slug for the category based on its name and ID
            category.slug = slugify(category_name) + '-' + str(category.id)

            # Save the category again with the updated slug
            category.save()

            # Display a success message
            messages.success(request, 'Category added successfully!')

            # Redirect the user to the 'menu_builder' page
            return redirect('menu_builder')
        else:
            # If the form is not valid, print the form errors
            print(form.errors)

    else:
        # If the request method is not POST, create a new form instance
        form = ProductCategoryForm()

    context = {
        'form': form,
    }

    # Render the 'add_product_category.html' template with the provided context
    return render(request, 'merchants/add_product_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def edit_product_category(request, pk=None):

    # Get the ProductCategory instance by its primary key (pk)
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':

        # Create a ProductCategoryForm instance with the POST data and the existing category instance
        form = ProductCategoryForm(request.POST, instance=category)

        if form.is_valid():

            # Extract the cleaned category name from the form data
            category_name = form.cleaned_data['category_name']
            
            # Create a category instance but don't save it to the database yet
            category = form.save(commit=False)
            
            # Set the merchant associated with this category
            category.merchant = get_merchant(request)
            
            # Generate a slug for the category based on the category name
            category.slug = slugify(category_name)
            
            # Save the category to the database
            form.save()
            
            # Display a success message and redirect to the menu builder page
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:

            # If the form is not valid, print the form errors to the console
            print(form.errors)

    else:
        # Create a ProductCategoryForm instance with the existing category instance
        form = ProductCategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    
    # Render the edit product category page with the form and category in the context
    return render(request, 'merchants/edit_product_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def delete_product_category(request, pk=None):
    # Get the ProductCategory instance by its primary key (pk)
    category = get_object_or_404(ProductCategory, pk=pk)
    
    # Delete the category
    category.delete()
    
    # Display a success message and redirect to the menu builder page
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')



@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def add_product_item(request):

    # Check if the request method is POST (form submission)
    if request.method == 'POST':

        # Create a form instance with POST data and uploaded files
        form = ProductItemForm(request.POST, request.FILES)

        # Check if the submitted form data is valid
        if form.is_valid():
            # Get the cleaned product title from the form
            product_title = form.cleaned_data['product_title']
            # Create a product instance but don't save it to the database yet
            product = form.save(commit=False)
            # Assign the logged-in merchant to the product
            product.merchant = get_merchant(request)
            # Generate a slug for the product based on its title
            product.slug = slugify(product_title)
            # Save the product to the database
            form.save()
            # Display a success message
            messages.success(request, 'Food Item added successfully!')
            # Redirect to the page displaying products of the same category
            return redirect('product_items_by_category', product.category.id)
        else:
            # Print form errors for debugging purposes
            print(form.errors)
    else:
        # If the request method is not POST, create an empty form
        form = ProductItemForm()

        # Filter product category options based on the logged-in merchant
        form.fields['category'].queryset = ProductCategory.objects.filter(merchant=get_merchant(request))
        
    context = {
        'form': form,
    }
    # Render the product item form page with the context
    return render(request, 'merchants/add_product_item.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def edit_product_item(request, pk=None):

    # Get the product to be edited based on the primary key (pk)
    product = get_object_or_404(ProductItem, pk=pk)

    if request.method == 'POST':
        # Create a form instance with POST data and uploaded files, pre-filled with the existing product data
        form = ProductItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Get the cleaned product title from the form
            product_title = form.cleaned_data['product_title']
            # Create a product instance but don't save it to the database yet
            product = form.save(commit=False)
            # Assign the logged-in merchant to the product
            product.merchant = get_merchant(request)
            # Generate a slug for the product based on its title
            product.slug = slugify(product_title)
            # Save the updated product to the database
            form.save()
            # Display a success message
            messages.success(request, 'Food Item updated successfully!')
            # Redirect to the page displaying products of the same category
            return redirect('product_items_by_category', product.category.id)
        else:
            # Print form errors for debugging purposes
            print(form.errors)

    else:
        # If the request method is not POST, create a form pre-filled with the existing product data
        form = ProductItemForm(instance=product)

        # Filter product category options based on the logged-in merchant
        form.fields['category'].queryset = ProductCategory.objects.filter(merchant=get_merchant(request))

    context = {
        'form': form,
        'product': product,
    }

    # Render the product item edit page with the context
    return render(request, 'merchants/edit_product_item.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def delete_product_item(request, pk=None):

    # Get the product to be deleted based on the primary key (pk)
    product = get_object_or_404(ProductItem, pk=pk)

    # Delete the product from the database
    product.delete()

    # Display a success message
    messages.success(request, 'Food Item has been deleted successfully!')
    
    # Redirect to the page displaying products of the same category
    return redirect('product_items_by_category', product.category.id)



def operating_hours(request):
    operating_hours = OperatingHour.objects.filter(merchant=get_merchant(request))
    form = OperatingHourForm()

    context = {
        'form': form,
        'operating_hours': operating_hours,
    }
    return render(request, 'merchants/operating_hours.html', context)

def add_operating_hours(request):
    # handle the data and save them inside the database
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            
            try:
                hour = OperatingHour.objects.create(merchant=get_merchant(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OperatingHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour+'-'+to_hour+' already exists for this day!'}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid request')

def remove_operating_hours(request, pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            hour = get_object_or_404(OperatingHour, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})
