from django.contrib import admin
from .models import Object, MoveObjects, TwistedTower

# Register your models here.
admin.site.register(Object)
admin.site.register(MoveObjects)
admin.site.register(TwistedTower)