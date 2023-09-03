##################
# django imports #
##################
from django.db import models


##########################################
#  import modules from current directory #
##########################################
from merchant.models import Merchant


#####################
# create class here #
#####################

class ProductCategory(models.Model):

    # Define a ForeignKey field named 'merchant' to associate each product category with a merchant (Merchant).
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'


    #####################
    # defined functions #
    #####################
    def clean(self):
        self.category_name = self.category_name.capitalize()
    
    def __str__(self):
        return self.category_name



# This class is associate with 2 other Models.
class ProductItem(models.Model):

    # ForeignKey relationship to the Merchant model
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    # ForeignKey relationship to the ProductCategory model with a custom related_name
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.CASCADE, 
        related_name='productitems')
    
    product_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='productimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    #####################
    # defined functions #
    #####################
    def __str__(self):
        return self.product_title
