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

    # Both path are separated for Customer and Merchant
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('merchantDashboard/', views.merchantDashboard, name='merchantDashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Password Reset / Forgot Password
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
