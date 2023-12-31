"""
URL configuration for Online_Food_Web_App_Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


##################
# django imports #
##################
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


##########################################
#  import modules from current directory #
##########################################
from . import views
from marketplace import views as MarketplaceViews


#####################
# url pattern lists #
#####################
urlpatterns = [

    # path for admin
    path('admin/', admin.site.urls),

    # path for functions inside views.py
    path('', views.home, name='home'),

    # When user go to 'accounts/' path. they have access to 'accounts app - urls.py'
    path('', include('accounts.urls')),

    path('marketplace/', include('marketplace.urls')),

    # Cart
    path('cart/', MarketplaceViews.cart, name='cart'),

    # SEARCH
    path('search/', MarketplaceViews.search, name='search'),

    # CHECKOUT
    path('checkout/', MarketplaceViews.checkout, name='checkout'),

    # ORDERS
    path('orders/', include('orders.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Above code is to append URL patterns for serving media files to your existing urlpatterns list