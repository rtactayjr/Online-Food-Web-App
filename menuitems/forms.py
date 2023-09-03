##################
# django imports #
##################
from django import forms
from accounts.validators import allow_only_images_validator

##########################################
#  import modules from current directory #
##########################################
from .models import ProductCategory, ProductItem

#####################
# create class here #
#####################
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category_name', 'description']


class ProductItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = ProductItem
        fields = ['category', 'product_title', 'description', 'price', 'image', 'is_available']