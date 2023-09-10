from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amounts
from menuitems.models import ProductItem
from .forms import OrderForm
from .models import Order, OrderedFood, Payment
import simplejson as json
from .utils import generate_order_number, order_total_by_merchant
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib.sites.shortcuts import get_current_site

# from Online_Food_Web_App_Main.settings import RZP_KEY_ID, RZP_KEY_SECRET
# Create your views here.

# client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))


@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
       return redirect('marketplace')

    merchants_ids = []
    for i in cart_items:
        if i.product_item.merchant.id not in merchants_ids:
            merchants_ids.append(i.product_item.merchant.id)
    
    # {"merchant_id":{"subtotal":{"tax_type": {"tax_percentage": "tax_amount"}}}}
    get_tax = Tax.objects.filter(is_active=True)

    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        product_item = ProductItem.objects.get(pk=i.product_item.id, merchant_id__in=merchants_ids)
        v_id = product_item.merchant.id
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (product_item.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (product_item.price * i.quantity)
            k[v_id] = subtotal
    
        # Calculate the tax_data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100, 2)
            tax_dict.update({tax_type: {str(tax_percentage) : str(tax_amount)}})
        # Construct total data
        total_data.update({product_item.merchant.id: {str(subtotal): str(tax_dict)}})


    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number = generate_order_number(order.id)
            order.merchants.add(*merchants_ids)
            order.save()

            # RazorPay Payment
            DATA = {
                "amount": float(order.total) * 100,
                "currency": "INR",
                "receipt": "receipt #"+order.order_number,
                "notes": {
                    "key1": "value3",
                    "key2": "value2"
                }
            }
            # rzp_order = client.order.create(data=DATA)
            # rzp_order_id = rzp_order['id']

            context = {
                'order': order,
                'cart_items': cart_items,
                # 'rzp_order_id': rzp_order_id,
                # 'RZP_KEY_ID': RZP_KEY_ID,
                'rzp_amount': float(order.total) * 100,
            }
            return render(request, 'orders/place_order.html', context)

        else:
            print(form.errors)
    return render(request, 'orders/place_order.html',)


def payments(request):
    pass

def order_complete(request):
    pass