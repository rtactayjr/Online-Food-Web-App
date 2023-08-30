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

    # Path is used for determining user role
    path('myAccount/', views.myAccount, name='myAccount'),

    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('merchantDashboard/', views.merchantDashboard, name='merchantDashboard'),
]
