##################
# django imports #
##################
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Prefetch

##########################################
#  import modules from current directory #
##########################################
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

    context = {
        'merchant': merchant,
        'categories': categories,
        # 'cart_items': cart_items,
        # 'opening_hours': opening_hours,
        # 'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/merchant_detail.html', context)


def increase_cart(request, product_id):
    pass

def decrease_cart(request, product_id):
    pass

def remove_cart(request, product_id):
    pass