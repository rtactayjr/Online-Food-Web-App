##################
# django imports #
##################
from django.urls import path, include


##########################################
#  import modules from current directory #
##########################################
from . import views


#####################
# url pattern LISTS #
#####################
urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    
    path('<slug:merchant_slug>/', views.merchant_detail, name='merchant_detail'),

    # ADD TO CART
    path('increase_cart/<int:product_id>/', views.increase_cart, name='increase_cart'),
    # DECREASE CART
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    # DELETE CART ITEM
    path('remove_cart/<int:cart_id>/', views.remove_cart, name='remove_cart'),
    
]