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
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('user', 'merchant_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'merchant_name')
    list_editable = ('is_approved',)


admin.site.register(Merchant, MerchantAdmin)