from django.contrib import admin
from .models import Efs, Used, StatusChange, Department, UserDepartment

admin.site.register(Efs)
admin.site.register(Used)
admin.site.register(StatusChange)
admin.site.register(Department)
admin.site.register(UserDepartment)