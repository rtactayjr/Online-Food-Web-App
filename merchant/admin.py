##################
# django imports #
##################
from django.contrib import admin

##########################################
#  import modules from current directory #
##########################################
from merchant.models import Merchant

#####################
# create class here #
#####################
# Define a custom admin class for the Merchant model
class MerchantAdmin(admin.ModelAdmin):
    
    # Display these fields in the list view of the admin panel
    list_display = ('user', 'merchant_name', 'is_approved', 'created_at')

    # Make the 'user' and 'merchant_name' fields in the list view clickable links
    list_display_links = ('user', 'merchant_name')

    # Allow editing of the 'is_approved' field directly in the list view
    list_editable = ('is_approved',)

# Register the Merchant model with the custom admin class
admin.site.register(Merchant, MerchantAdmin)