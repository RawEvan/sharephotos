from django.contrib import admin

# Register your models here.
from sharephotos.models import tb_photo, tb_tag

admin.site.register(tb_photo)
admin.site.register(tb_tag)
