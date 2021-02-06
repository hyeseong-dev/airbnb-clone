from math                  import ceil
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts      import render, redirect
from rooms                 import models

def all_rooms(request):
    page      = request.GET.get('page',1)
    
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5) # orphans를 넣게 되면 그 이하로 된 걸 이전페이지에 넣게 된다. 이경우 11페이지에 1개만 있던걸 10페이지에 11개를 가지게함. 
    try:
        rooms = paginator.page(int(page))
        return render(request, 'rooms/home.html', {'page':rooms})
    except EmptyPage:
        rooms = paginator.page(1)
        return redirect('/') #  ?page=12312376878912 과 같이 shiity page 나오면 아예 메인 페이지로 리다이렉트 시켜 url 리셋해버림

