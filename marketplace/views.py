##################
# django imports #
##################
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch
from django.db.models import Q

from django.contrib.auth.decorators import login_required

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
from datetime import date, datetime

##########################################
#  import modules from current directory #
##########################################
from . models import Cart
from . context_processors import get_cart_counter, get_cart_amounts

from merchant.models import Merchant, OperatingHour
from menuitems.models import ProductCategory, ProductItem
from accounts.models import UserProfile
from orders.forms import OrderForm

#############################
# defined functions - views #
#############################

def marketplace(request):
    # Retrieve a list of approved and active merchants
    merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)

    # Count the number of merchants
    merchant_count = merchants.count()

    # Create a context dictionary with the retrieved data
    context = {
        'merchants': merchants,
        'merchant_count': merchant_count,
    }

    # Render the 'product_listings.html' template with the provided context
    return render(request, 'marketplace/product_listings.html', context)


def merchant_detail(request, merchant_slug):
    # Retrieve the merchant object with the given merchant_slug
    merchant = get_object_or_404(Merchant, merchant_slug=merchant_slug)

    # Fetch all product categories associated with the merchant and prefetch related product items
    categories = ProductCategory.objects.filter(merchant=merchant).prefetch_related(
        Prefetch('productitems',
                queryset=ProductItem.objects.filter(is_available=True)
        )
    )

    operating_hours = OperatingHour.objects.filter(merchant=merchant).order_by('day', 'from_hour')

    # Check current day's opening hours.
    today_date = date.today()
    today = today_date.isoweekday()

    current_operating_hours = OperatingHour.objects.filter(merchant=merchant, day=today)
    
    # Check if the user is authenticated, and retrieve their cart items if so
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    # Create a context dictionary with the retrieved data
    context = {
        'merchant': merchant,
        'categories': categories,
        'cart_items': cart_items,
        'operating_hours': operating_hours,
        'current_operating_hours': current_operating_hours,
    }

    # Render the 'merchant_detail.html' template with the provided context
    return render(request, 'marketplace/merchant_detail.html', context)


def increase_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                product_item = ProductItem.objects.get(id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product_item=product_item)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Increased the cart quantity', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(
                                                user=request.user, 
                                                product_item=product_item, 
                                                quantity=1)
                    
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Added the food to the cart', 
                        'cart_counter': get_cart_counter(request), 
                        'qty': chkCart.quantity, 
                        'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({
                    'status': 'Failed', 
                    'message': 'This food does not exist!'})
        else:
            return JsonResponse({
                'status': 'Failed', 
                'message': 'Invalid request!'})
    else:
        return JsonResponse({
            'status': 'login_required', 
            'message': 'Please login to continue'})


def decrease_cart(request, product_id):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Check if the request is AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Get the product item associated with the given product_id
                product_item = ProductItem.objects.get(id=product_id)

                try:
                    # Check if the product item is already in the user's cart
                    chkCart = Cart.objects.get(user=request.user, product_item=product_item)

                    if chkCart.quantity > 1:
                        # Decrease the cart quantity if it's greater than 1
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        # If the quantity is 1 or less, remove the cart item
                        chkCart.delete()
                        chkCart.quantity = 0

                    # Return a JSON response with updated cart information
                    return JsonResponse({
                        'status': 'Success',
                        'cart_counter': get_cart_counter(request),
                        'qty': chkCart.quantity,
                        'cart_amount': get_cart_amounts(request)
                    })
                except:
                    # If the product item is not in the cart, return a failure JSON response
                    return JsonResponse({'status': 'Failed', 
                                         'message': 'You do not have this item in your cart!'})
            except:
                # If the product does not exist, return a failure JSON response
                return JsonResponse({'status': 'Failed', 
                                     'message': 'This food does not exist!'})
        else:
            # If the request is not AJAX, return a failure JSON response
            return JsonResponse({'status': 'Failed', 
                                 'message': 'Invalid request!'})
    else:
        # If the user is not authenticated, return a JSON response indicating the need to log in
        return JsonResponse({'status': 'login_required', 
                             'message': 'Please login to continue'})

    

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'marketplace/cart.html', context)

def remove_cart(request, cart_id):
      if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({
                        'status': 'Success', 
                        'message': 'Cart item has been deleted!', 
                        'cart_counter': get_cart_counter(request), 
                        'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        

def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

        get_merchants_by_product_item = ProductItem.objects.filter(product_title__icontains=keyword, is_available=True).values_list('merchant', flat=True)

        merchants = Merchant.objects.filter(Q(id__in=get_merchants_by_product_item) | Q(merchant_name__icontains=keyword, is_approved=True, user__is_active=True))

        if latitude and longitude and radius:
                pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

                merchants = Merchant.objects.filter(Q(id__in=get_merchants_by_product_item) | Q(merchant_name__icontains=keyword, is_approved=True, user__is_active=True),
                user_profile__location__distance_lte=(pnt, D(km=radius))
                ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

                for m in merchants:
                    m.kms = round(m.distance.km, 1)

    # merchants = Merchant.objects.filter(merchant_name__icontains=keyword, is_approved=True, user__is_active=True)
    merchant_count = merchants.count()

    context = {
        'merchants': merchants,
        'merchant_count': merchant_count,
        'source_location': address,
    }

    return render(request, 'marketplace/listings.html', context)


@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/checkout.html', context)
