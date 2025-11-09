from django.contrib import admin
from .models import *

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ["name", "position__position_name", "status__status_name", "department__department_name"]
    autocomplete_fields  = ["position", "status", "department"]
    list_filter = ["position__position_name", "status__status_name", "department__department_name"]
admin.site.register(EmployeeModel, EmployeeAdmin)

class PositionAdmin(admin.ModelAdmin):
    search_fields = ["position_name"]
admin.site.register(PositionModel, PositionAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["department_name"]
admin.site.register(DepartmentModel, DepartmentAdmin)

class StatusAdmin(admin.ModelAdmin):
    search_fields = ["status_name"]
admin.site.register(StatusModel, StatusAdmin)

