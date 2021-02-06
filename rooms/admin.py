from django.contrib          import admin
from django.utils.safestring import mark_safe

from rooms                   import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRules)
class ItemAdmin(admin.ModelAdmin):

    """ ItemAdmin  Admin Definition"""
    
    list_display = ('name','used_by')

    def used_by(self, obj):
        return obj.rooms.count()

class PhotoInline(admin.TabularInline):
# class PhotoInline(admin.StackedInline): 세로로 길게 표현함

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    
    """ RoomAdmin  Admin Definition"""

    inlines = (PhotoInline,)

    fieldsets = (
        (
          "Basic Info",
                                 {"fields": ("name", "description", "country",'city', "address","price")}
        ), # 마지막에 콤마 안붙이면 서버 죽어버림
        ("Times",                {"fields": ("check_in", "check_out", "instant_book")}), 
        ("Spaces",               {"fields": ("guests", "beds", "bedrooms", "baths",)}), 
                                 
        ("More About The Space", {
                                 "classes": ("collapse",),
                                 "fields": ("amenities", "facilities", "house_rules")
                                 }), 
        ("Last Details",         {"fields": ("host",)}), 
         
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
                        "name",
                        "country",
                        "city",
                        "price",
                        "address",
                        "guests",
                        "beds",
                        "baths",
                        "check_in",
                        "check_out",
                        "instant_book",
                        "count_amenities",
                        'count_photos',
                        'total_rating',
    )

    list_filter = (
                        'host__superhost',
                        'instant_book',
                        'room_type',
                        'amenities',
                        'facilities',
                        'house_rules',
                        'city',
                        'country',
    )

    raw_id_fields = ("host",)
    search_fields = ('=city', '^host__username', )
    filter_horizontal = ('amenities', 'facilities', 'house_rules',) # 수평 필터링은 MTM 관계에서 잘 작동함


    # def save_model(self, request, obj, form, change): # 어드민에서만 작업하고 싶은 경우 지엽적으로 사용
    #     print(obj, change, form)
    #     super().save_model(request, obj, form, change)

    def count_amenities(self, obj):        
        return obj.amenities.count()
    count_amenities.short_description = "Amenity Count"

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "Photo Count"
    

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """ PhotoAdmin  Admin Definition"""

    list_display = ('__str__', 'get_thumbnail')

    def get_thumbnail(self,obj):
        return mark_safe(f"<img width='50px' src='{obj.file.url}' />")

    get_thumbnail.short_description = 'Thumbnail'