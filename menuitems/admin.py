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
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'merchant', 'updated_at')
    search_fields = ('category_name', 'merchant__merchant_name')


class ProductItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_title',)}
    list_display = ('product_title', 'category', 'merchant', 'price', 'is_available', 'updated_at')
    search_fields = ('product_title', 'category__category_name', 'merchant__merchant_name', 'price')
    list_filter = ('is_available',)


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductItem, ProductItemAdmin)