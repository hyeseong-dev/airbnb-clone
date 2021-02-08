from django.utils          import timezone
from django.shortcuts      import render, redirect
from django.urls           import reverse
from django.views.generic  import ListView, DetailView

from django_countries      import countries

from rooms                 import models


class HomeView(ListView):
    
    ''' HomeView Definition '''

    model               = models.Room
    paginate_by         = 10
    paginate_orphans    = 5
    ordering            = 'created'
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context        = super().get_context_data(**kwargs)
        now            = timezone.now()
        context['now'] = now
        return context


class RoomDetail(DetailView):
    
    ''' RoomDetail Definition '''
    
    model = models.Room


def search(request):
    print((request.GET))
    city             = request.GET.get('city','Anywhere')
    city             = str.capitalize(city)
    s_country        = request.GET.get('country','KR')
    room_type_1st_id = models.RoomType.objects.values('pk').first()['pk']
    s_room_type      = int(request.GET.get('room_type',room_type_1st_id))
    
    price        = int(request.GET.get('price'     , 0))
    guests       = int(request.GET.get('guests'    , 0))
    bedrooms     = int(request.GET.get('bedrooms'  , 0))
    beds         = int(request.GET.get('beds'      , 0))
    baths        = int(request.GET.get('baths'     , 0))
    s_amenities  = request.GET.get('amenities' )
    s_facilities = request.GET.get('facilities')
    print(s_amenities, s_facilities)
    

    form = {
        'city'       : city       ,
        's_room_type': s_room_type,
        's_country'  : s_country  ,
        'price'      : price      ,
        'guests'     : guests     ,
        'bedrooms'   : bedrooms   ,
        'beds'       : beds       ,
        'baths'      : baths      ,
    }

    room_types = models.RoomType.objects.all()
    amenities  = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        'countries'  : countries  ,
        'room_types' : room_types ,
        'room_types' : room_types ,
        'amenities'  : amenities  ,
        'facilities' : facilities ,
    }

    return render(request, 'rooms/search.html', context={**form, **choices})