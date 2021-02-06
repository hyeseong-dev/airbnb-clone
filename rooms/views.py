from django.shortcuts import render

from rooms            import models

def all_rooms(request):
    page      = int(request.GET.get('page',0))
    page_size = 10
    limit     = page_size * page    # limit  = 
    offset    = limit - page_size

    rooms = models.Room.objects.all()[offset:limit]

    return render(request, 'rooms/homes.html', context={
    'rooms': rooms,
    
    })
