##################
# django imports #
##################
from django.db import models

##########################################
#  import modules from current directory #
##########################################
from accounts.models import CustomUser
from menuitems.models import ProductItem


#####################
# create class here #
#####################
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user

class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type