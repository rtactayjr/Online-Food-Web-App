##################
# django imports #
##################
from django.urls import path, include


##########################################
#  import modules from current directory #
##########################################
from . import views
from accounts import views as AccountViews


#####################
# url pattern LISTS #
#####################
urlpatterns = [

    # URL for the Merchant Dashboard view
    path('', AccountViews.merchantDashboard, name='merchantDashboard'),

    # URL for the Merchant Profile view
    path('profile/', views.merchantProfile, name='merchantProfile'),

    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/product-items-category/<int:pk>/', views.product_items_by_category, name='product_items_by_category'),

    # Product Category CRUD
    path('menu-builder/product-items-category/add/', views.add_product_category, name='add_product_category'),
    path('menu-builder/product-items-category/edit/<int:pk>/', views.edit_product_category, name='edit_product_category'),
    path('menu-builder/product-items-category/delete/<int:pk>/', views.delete_product_category, name='delete_product_category'),

    # Product Item CRUD
    path('menu-builder/product/add/', views.add_product_item, name='add_product_item'),
    path('menu-builder/product/edit/<int:pk>/', views.edit_product_item, name='edit_product_item'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product_item, name='delete_product_item'),

    # # Opening Hour CRUD
    # path('opening-hours/', views.opening_hours, name='opening_hours'),
    # path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    # path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    # path('my_orders/', views.my_orders, name='vendor_my_orders'),

]
