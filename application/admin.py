from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(doctors)
admin.site.register(department)
admin.site.register(appointment)
admin.site.register(fakes)