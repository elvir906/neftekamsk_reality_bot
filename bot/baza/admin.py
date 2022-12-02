from django.contrib import admin

from .models import Apartment, House, Land, Room, TownHouse


class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        'room_quantity',
        'street_name',
        'number_of_house',
        'floor',
        'number_of_floors',
        'area',
        'description',
        'encumbrance',
        'children',
        'mortage',
        'price',
        'pub_date',
        'author',
        'phone_number',
        'agency',
    )


class RoomAdmin (admin.ModelAdmin):
    list_display = (
        'street_name',
        'number_of_house',
        'floor',
        'number_of_floors',
        'area',
        'description',
        'encumbrance',
        'children',
        'mortage',
        'price',
        'pub_date',
        'author',
        'phone_number',
        'agency_name',
    )


class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'microregion',
        'street_name',
        'area',
        'area_of_land',
        'purpose',
        'material',
        'finish',
        'gaz',
        'water',
        'road',
        'description',
        'sauna',
        'garage',
        'fence',
        'encumbrance',
        'children',
        'mortage',
        'price',
        'pub_date',
        'author',
        'phone_number',
        'agency_name',
    )


class TownHouseAdmin(admin.ModelAdmin):
    list_display = (
        'microregion',
        'street_name',
        'area',
        'area_of_land',
        'purpose',
        'material',
        'finish',
        'gaz',
        'water',
        'road',
        'description',
        'sauna',
        'garage',
        'fence',
        'encumbrance',
        'children',
        'mortage',
        'price',
        'pub_date',
        'author',
        'phone_number',
        'agency_name',
    )


class LandAdmin(admin.ModelAdmin):
    list_daisplay = (
        'microregion',
        'street_name',
        'area_of_land',
        'purpose',
        'gaz',
        'water',
        'road',
        'description',
        'fence',
        'encumbrance',
        'children',
        'mortage',
        'price',
        'pub_date',
        'author',
        'phone_number',
        'agency_name',
    )


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(TownHouse, TownHouseAdmin)
admin.site.register(Land, LandAdmin)
