##################
# django imports #
##################
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify


##########################################
#  import modules from current directory #
##########################################
from . forms import MerchantForm
from . models import Merchant

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

# Function to get the current logged in Merchant
def get_merchant(request):
    merchant = Merchant.objects.get(user=request.user)
    return merchant

@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def menu_builder(request):

    # Get the Logged in Merchant
    merchant = get_merchant(request)

    # Get all the Product Category of the merchant, ordered by 'created_at'
    categories = ProductCategory.objects.filter(merchant=merchant).order_by('created_at')

    # Pass the values of 'categories' as context
    context = {
        'categories': categories,
    }

    # Pass the context to html page.
    return render(request, 'merchants/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def productitems_by_category(request, pk=None):
    merchant = get_merchant(request)
    category = get_object_or_404(ProductCategory, pk=pk)
    productitems = ProductItem.objects.filter(merchant=merchant, category=category)

    context = {
        'productitems': productitems,
        'category': category,
    }

    return render(request, 'merchants/productitems_by_category.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def add_product_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.merchant = get_merchant(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = ProductCategoryForm()

    context = {
        'form': form,
    }
    return render(request, 'merchants/add_product_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def edit_product_category(request, pk=None):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)

        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.merchant = get_merchant(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)

    else:
        form = ProductCategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    
    return render(request, 'merchants/edit_product_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_merchant)
def delete_product_category(request, pk=None):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menu_builder')