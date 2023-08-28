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

    path('registerCustomer/', views.registerCustomer, name='registerCustomer')

]
