from django.contrib    import admin

from rooms              import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRules)
class ItemAdmin(admin.ModelAdmin):

    """ ItemAdmin  Admin Definition"""
    
    list_display = ('name','used_by')

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    
    """ RoomAdmin  Admin Definition"""

    fieldsets = (
        (
          "Basic Info",
                                 {"fields": ("name", "description", "country", "address","price")}
        ), # 마지막에 콤마 안붙이면 서버 죽어버림
        ("Spaces",               {"fields": ("guests", "beds", "bedrooms", "baths",)}), 
        ("Times",                {"fields": ("check_in", "check_out")}), 
                                 
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

    filter_horizontal = (
                            'amenities',  
                            'facilities', 
                            'house_rules',
    ) # 수평 필터링은 MTM 관계에서 잘 작동함

    search_fields = (
                        '=city', '^host__username',
    )

    def count_amenities(self, obj):        
        return obj.amenities.count()
    # count_amenities.short_description = 'hello sexy!'

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """ PhotoAdmin  Admin Definition"""

    pass
