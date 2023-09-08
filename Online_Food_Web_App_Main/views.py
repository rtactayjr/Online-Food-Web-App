##################
# django imports #
##################
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance


from merchant.models import Merchant

#####################
# defined functions #
#####################
def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None
    
def home(request):
    if get_or_set_current_location(request) is not None:
        pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))
        merchants = Merchant.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1000))).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")
        for m in merchants:
            m.kms = round(m.distance.km, 1)
    else:
        # Retrieve a list of approved and active merchants (up to 8) for display on the home page
        merchants = Merchant.objects.filter(is_approved=True, user__is_active=True)[:8]
  
    # Create a context dictionary to pass data to the template
    context = {
        'merchants': merchants,  # Provide the list of merchants to the template
    }
 
    # Render the 'home.html' template with the provided context
    return render(request, 'home.html', context)
