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
        db_table     = 'room_types'

    def __str__(self):
        return self.name



class Facility(AbstractItem):

    ''' Facility Object Definition''' 

    class Meta:
        verbose_name_plural = 'Facilities'
        db_table     = 'facilities'
    
    def __str__(self):
        return self.name


class HouseRules(AbstractItem):

    ''' HouseRules Object Definition''' 

    class Meta:
        verbose_name = 'House Rule'
        db_table     = 'house_rules'

    def __str__(self):
        return self.name


class Amenity(AbstractItem):

    ''' Amenity Object Definition''' 

    class Meta:
        verbose_name_plural = 'Amenities'
        db_table            = 'amenities'

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):
    
    ''' Photo Model Definition'''

    caption = models.CharField(max_length=80)
    file    = models.ImageField(upload_to='room_photos')
    room    = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return self.caption
    
    class Meta:
        db_table = 'photos'

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

    def save(self, *args, **kwargs):
        # self.city = self.city[0].upper()+self.city[1:] 코드가 길어지는 문제
        self.city = self.city.title() # str의 title() 메소드를 사용하여 각 단어의 첫글자를 대문자로 만듬
        super().save(*args, **kwargs)

    def total_rating(self):
        all_reviews   = self.reviews.all()
        total_sum     = sum([review.rating_average() for review in all_reviews])
        
        if all_reviews.exists():
            total_average = total_sum / all_reviews.count() 
            return round(total_average, 2)
        return 0

    class Meta:
        db_table            = 'rooms'

