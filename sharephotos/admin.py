from django.contrib import admin

# Register your models here.
from sharephotos.models import tb_photo_info, tb_tag

admin.site.register(tb_photo_info)
admin.site.register(tb_tag)
