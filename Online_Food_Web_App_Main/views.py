##################
# django imports #
##################
from django.shortcuts import render
from django.http import HttpResponse

#####################
# defined functions #
#####################
def home(request):
    return render(request, 'home.html')