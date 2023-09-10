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

    # URL for the default user landing page, redirects based on user role
    path('', views.myAccount, name='myAccount'),

    # URL for registering a new customer
    path('registerCustomer/', views.registerCustomer, name='registerCustomer'),

    # URL for registering a new merchant
    path('registerMerchant/', views.registerMerchant, name='registerMerchant'),

    # URLs for user authentication: login and logout
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # URL for determining user role (used internally)
    path('myAccount/', views.myAccount, name='myAccount'),

    # URLs for Customer and Merchant Dashboards
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('merchantDashboard/', views.merchantDashboard, name='merchantDashboard'),

    # URL for user account activation
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # URLs for password reset/forgot password functionality
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # URL for accessing the "Merchant" app (including its own URLs)
    path('merchant/', include('merchant.urls')),
    path('customer/', include('customers.urls')),
]
