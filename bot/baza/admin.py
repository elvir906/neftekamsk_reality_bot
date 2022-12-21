from django.contrib import admin

from .models import (Apartment, House, Individuals, Land, Room, Subscriptors,
                     TownHouse)


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
        'code_word',
        'photo_id',
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
        'code_word',
        'photo_id',
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
        'code_word',
        'photo_id',
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
        'code_word',
        'photo_id',
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
        'code_word',
        'photo_id',
    )


class SubscriptorsAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'agency_name'
    )


class IndividualsAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'name'
    )


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(TownHouse, TownHouseAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(Subscriptors, SubscriptorsAdmin)
admin.site.register(Individuals, IndividualsAdmin)
