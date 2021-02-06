from django.urls import path
from rooms       import views

app_name = 'rooms'

urlpatterns = [
    path('<int:pk>', views.room_detail, name='detail')
]
