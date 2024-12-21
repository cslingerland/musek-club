from django.contrib import admin

# Register your models here.

from .models import Club, Pick

admin.site.register(Club)
admin.site.register(Pick)