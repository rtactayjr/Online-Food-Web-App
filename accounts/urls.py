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

    path('registerUser/', views.registerUser, name='registerUser')

]
