from django.db import models

from django_countries.fields import CountryField

from core         import models as core_models


class AbstractItem(core_models.TimeStampedModel):
    
    ''' Item Model Definition''' 

    name = models.CharField(max_length=80)
    
    class Meta:
        abstract = True
    
    def  __str__(self):
        return self.name


class RoomType(AbstractItem):

    ''' RoomType Object Definition''' 
    class Meta:
        verbose_name = 'Room Type'


class Facility(AbstractItem):

    ''' Facility Object Definition''' 

    class Meta:
        verbose_name_plural = 'Facilities'


class HouseRules(AbstractItem):

    ''' HouseRules Object Definition''' 

    class Meta:
        verbose_name = 'House Rule'


class Amenity(AbstractItem):

    ''' Amenity Object Definition''' 

    class Meta:
        verbose_name_plural = 'Amenities'


class Room(core_models.TimeStampedModel):
    
    ''' Room Model Definition'''

    name            = models.CharField(max_length=140)
    description     = models.TextField()
    country         = CountryField()
    city            = models.CharField(max_length=80)
    price           = models.IntegerField()
    address         = models.CharField(max_length=140)
    guests          = models.IntegerField()
    beds            = models.IntegerField()
    baths           = models.IntegerField()
    bedrooms        = models.IntegerField()
    check_in        = models.TimeField()                           # 0~24시간 표기를 위함
    check_out       = models.TimeField()
    instant_book    = models.BooleanField(default=False)   # 즉시 예약 가능 유무
    host            = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='rooms')
    room_type       = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True, related_name='rooms')
    amenities       = models.ManyToManyField('Amenity', blank=True, related_name='rooms')
    facilities      = models.ManyToManyField('Facility', blank=True, related_name='rooms')
    house_rules     = models.ManyToManyField('HouseRules', blank=True, related_name='rooms')

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews   = self.reviews.all()
        total_sum     = sum([review.rating_average() for review in all_reviews])
        total_average = total_sum / all_reviews.count() 
        return round(total_average, 2)


class Photo(core_models.TimeStampedModel):
    
    ''' Photo Model Definition'''

    caption = models.CharField(max_length=80)
    file    = models.ImageField(upload_to='room_photos')
    room    = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='photos')
