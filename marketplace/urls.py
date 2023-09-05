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

    # # ADD TO CART
    # path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    # # DECREASE CART
    # path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    # # DELETE CART ITEM
    # path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    
]