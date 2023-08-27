##################
# django imports #
##################
from django.http import HttpResponse
from django.shortcuts import render


#############################
# defined functions - views #
#############################

def registerUser(request):
    return HttpResponse('This is the registration form')