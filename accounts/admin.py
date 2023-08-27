##################
# django imports #
##################
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


##########################################
#  import modules from current directory #
##########################################
from . models import CustomUser, UserProfile


#####################
# create class here #
#####################

# Intended to customize the behavior and appearance of the Django admin interface for managing instances of the 'CustomUser' model
class CustomUserAdmin(UserAdmin):

    """
    - Arrange how the user data will show up.
    - Retrive the models in desc order based on 'date_joined'
    - Show the fields as a vertical list.
    - Used to specify fields that should be displayed as filters on the right side of the admin list view.
    - Control the layout and structure of the form used to edit user details in the admin interface.
    """
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    #####################
    # defined functions #
    #####################

# Integrate the CustomUser model with the Django admin interface,
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)