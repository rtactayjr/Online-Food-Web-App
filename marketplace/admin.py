##################
# django imports #
##################
from django.contrib import admin

##########################################
#  import modules from current directory #
##########################################
from .models import Cart, Tax

#####################
# create class here #
#####################
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_item', 'quantity', 'updated_at')

class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


# Integrate the Cart/Tax model with the Django admin interface,
admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)