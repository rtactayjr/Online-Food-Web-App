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
    """
    Form for creating and updating product categories.

    Attributes:
        category_name (CharField): The name of the product category.
        description (CharField): A brief description of the product category.
    """
    class Meta:
        model = ProductCategory
        fields = ['category_name', 'description']


class ProductItemForm(forms.ModelForm):
    """
    Form for creating and updating product items.

    Attributes:
        image (FileField): The image representing the product item.
        category (ForeignKey): The category to which the product item belongs.
        product_title (CharField): The title of the product item.
        description (CharField): A brief description of the product item.
        price (DecimalField): The price of the product item.
        is_available (BooleanField): Indicates whether the product item is available for purchase.
    """
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = ProductItem
        fields = ['category', 'product_title', 'description', 'price', 'image', 'is_available']
