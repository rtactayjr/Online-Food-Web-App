##################
# django imports #
##################
from django.urls import path


##########################################
#  import modules from current directory #
##########################################
from . import views


#####################
# url pattern LISTS #
#####################
urlpatterns = [

    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),

    # Adding Merchant Path
    path('registerMerchant/', views.registerMerchant, name='registerMerchant')

]
