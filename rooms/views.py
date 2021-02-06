from math             import ceil

from django.shortcuts import render

from rooms            import models

def all_rooms(request):
    page      = request.GET.get('page',1)
    page      = int(page or 1)

    PAGE_SIZE = 10
    limit     = PAGE_SIZE * page    # limit  = 
    offset    = limit - PAGE_SIZE

    rooms      = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count()/PAGE_SIZE)

    return render(
        request, 
        'rooms/homes.html', 
        context={
            'rooms'      : rooms,
            'page'       : page,
            'page_count' : page_count,
            'page_range' : range(1, page_count),
        },)
