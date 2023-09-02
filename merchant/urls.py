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


    # path('menu-builder/', views.menu_builder, name='menu_builder'),
    # path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # # Category CRUD
    # path('menu-builder/category/add/', views.add_category, name='add_category'),
    # path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    # path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # # FoodItem CRUD
    # path('menu-builder/food/add/', views.add_food, name='add_food'),
    # path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    # path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # # Opening Hour CRUD
    # path('opening-hours/', views.opening_hours, name='opening_hours'),
    # path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    # path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    # path('my_orders/', views.my_orders, name='vendor_my_orders'),

]
