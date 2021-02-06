from math                  import ceil
from django.core.paginator import Paginator
from django.shortcuts      import render
from rooms                 import models

def all_rooms(request):
    page      = request.GET.get('page')
    
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)

    print(vars(rooms.paginator) )
    return render(
        request, 
        'rooms/homes.html', 
        context = {
            'rooms':rooms,
        }
        )

