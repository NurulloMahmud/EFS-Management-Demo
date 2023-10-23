from django.contrib import admin
from .models import Efs, Used, StatusChange

admin.site.register(Efs)
admin.site.register(Used)
admin.site.register(StatusChange)