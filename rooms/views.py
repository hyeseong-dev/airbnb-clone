from django.views.generic  import ListView
from rooms                 import models

class HomeView(ListView):
    
    ''' HomeView Definition '''

    model            = models.Room
    paginate_by      = 10
    paginate_orphans = 5
    ordering         = 'created'