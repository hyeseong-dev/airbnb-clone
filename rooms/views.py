from math                  import ceil
from django.core.paginator import Paginator
from django.shortcuts      import render
from rooms                 import models

def all_rooms(request):
    page      = request.GET.get('page',1)
    
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5) # orphans를 넣게 되면 그 이하로 된 걸 이전페이지에 넣게 된다. 이경우 11페이지에 1개만 있던걸 10페이지에 11개를 가지게함. 
    rooms = paginator.page(int(page))

    return render(
        request, 
        'rooms/homes.html', 
        context = {
            'page':rooms,
        }
        )

