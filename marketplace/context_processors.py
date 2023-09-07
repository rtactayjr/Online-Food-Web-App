from . models import Cart, Tax
from menuitems.models import ProductItem


def get_cart_counter(request):
    # Initialize the cart_count to 0
    cart_count = 0

    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the cart items associated with the authenticated user
            cart_items = Cart.objects.filter(user=request.user)

            # If there are cart items, calculate the total quantity in the cart
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                # If there are no cart items, set cart_count to 0
                cart_count = 0
        except:
            # Handle exceptions gracefully by setting cart_count to 0
            cart_count = 0

    # Return the cart_count as a dictionary
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    # Initialize variables to calculate cart amounts
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve cart items for the authenticated user
        cart_items = Cart.objects.filter(user=request.user)
        
        # Calculate the subtotal by summing up the product pr
        # ices multiplied by quantities
        for item in cart_items:
            product_item = ProductItem.objects.get(pk=item.product_item.id)
            subtotal += (product_item.price * item.quantity)

        # Retrieve active tax rates and calculate tax amounts
        get_tax = Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal) / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})
        
        # Calculate the total tax amount
        tax = sum(x for key in tax_dict.values() for x in key.values())
        
        # Calculate the grand total by adding the subtotal and tax
        grand_total = subtotal + tax

    # Return cart amounts and tax details as a dictionary
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)
