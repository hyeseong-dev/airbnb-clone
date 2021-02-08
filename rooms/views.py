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
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


class RoomDetail(DetailView):
    
    model = models.Room


def search(request):
    print((request.GET))
    city = request.GET.get('city','Anywhere')
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()

    return render(request, 'rooms/search.html', context={'city':city, 'countries' : countries, 'room_types':room_types })