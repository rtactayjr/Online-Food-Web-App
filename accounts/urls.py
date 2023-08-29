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

    # Adding Customer login page
    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),

    # Adding Merchant login page
    path('registerMerchant/', views.registerMerchant, name='registerMerchant'),

    # Adding Login/Logout Path
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Add path to Dashboard, will be viewed once User is logged in
    path('dashboard/', views.dashboard, name='dashboard'),
]
