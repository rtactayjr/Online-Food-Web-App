##################
# django imports #
##################
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch

##########################################
#  import modules from current directory #
##########################################
from . models import Cart
from .context_processors import get_cart_counter, get_cart_amounts

from merchant.models import Merchant
from menuitems.models import ProductCategory, ProductItem

#############################
# defined functions - views #
#############################

def marketplace(request):
    merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)
    merchant_count = merchants.count()

    context = {
        'merchants': merchants,
        'merchant_count': merchant_count,
    }

    return render(request, 'marketplace/product_listings.html', context)


def merchant_detail(request, merchant_slug):
    merchant = get_object_or_404(Merchant, merchant_slug=merchant_slug)

    categories = ProductCategory.objects.filter(merchant=merchant).prefetch_related(
                    Prefetch(
                        'productitems',
                        queryset = ProductItem.objects.filter(is_available=True)
                    )
                )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    context = {
        'merchant': merchant,
        'categories': categories,
        'cart_items': cart_items,
        # 'opening_hours': opening_hours,
        # 'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/merchant_detail.html', context)


def increase_cart(request, product_id):
    if request.user.is_authenticated:

        # Condition to check whether the request is 'AJAX'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
             #Check if the food item exists
            try:
                product_item = ProductItem.objects.get(id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product_item=product_item)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, product_item=product_item, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the Product to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This Product does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                product_item = ProductItem.objects.get(id=product_id)
                # Check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, product_item=product_item)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    

def remove_cart(request, product_id):
    pass