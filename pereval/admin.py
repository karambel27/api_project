from django.contrib import admin

from .models import User, Coords, Level, PerevalAdded, Image


admin.site.register(User)
admin.site.register(Coords)
admin.site.register(Level)
admin.site.register(PerevalAdded)
admin.site.register(Image)
