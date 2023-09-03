##################
# django imports #
##################
from django.contrib import admin

##########################################
#  import modules from current directory #
##########################################
from .models import ProductCategory, ProductItem

#####################
# create class here #
#####################
class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Admin class for managing product categories.

    Attributes:
        prepopulated_fields (dict): Automatically generates the 'slug' field based on 'category_name'.
        list_display (tuple): Specifies the fields to display in the list view of the admin panel.
        search_fields (tuple): Specifies the fields to search for in the admin panel's search bar.
    """
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'merchant', 'updated_at')
    search_fields = ('category_name', 'merchant__merchant_name')


class ProductItemAdmin(admin.ModelAdmin):
    """
    Admin class for managing product items.

    Attributes:
        prepopulated_fields (dict): Automatically generates the 'slug' field based on 'product_title'.
        list_display (tuple): Specifies the fields to display in the list view of the admin panel.
        search_fields (tuple): Specifies the fields to search for in the admin panel's search bar.
        list_filter (tuple): Specifies the fields to use as filters in the admin panel.
    """
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'merchant', 'price', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name', 'merchant__merchant_name', 'price')
    list_filter = ('is_available',)

# Register the admin classes
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
