from django.contrib import admin

# Register your models here.
from sharephotos.models import Photo, Tag, Interest, Collect, Authority, Similarity

admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Interest)
admin.site.register(Collect)
admin.site.register(Authority)
admin.site.register(Similarity)
