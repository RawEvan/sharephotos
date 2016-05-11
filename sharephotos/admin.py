from django.contrib import admin

# Register your models here.
from sharephotos.models import Photo, Tag

admin.site.register(Photo)
admin.site.register(Tag)
