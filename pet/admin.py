from django.contrib import admin

from announcement.models import Announcement
from pet.models import Breed, Pet, Picture


class PetPictureInline(admin.StackedInline):
    model = Pet.pictures.through
    raw_id_fields = ('picture',)
    extra = 0


class PetAnnouncementInline(admin.StackedInline):
    model = Announcement
    classes = ('collapse',)
    extra = 0


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('kind', 'date_added')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name', 'kind')}


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sex', 'kind', 'breed', 'user',
    )
    exclude = ('pictures',)
    readonly_fields = ('slug',)
    list_filter = (
        'sex',
        'kind',
        'breed',
    )
    search_fields = ('name', 'description')
    raw_id_fields = ('picture', 'breed', 'user')
    inlines = (PetPictureInline, PetAnnouncementInline)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'date_added')
    list_filter = ('date_added', 'date_changed')
    readonly_fields = ('original_file_name',)
