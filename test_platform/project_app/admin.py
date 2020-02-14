from django.contrib import admin
from project_app.models import Project,Module

# Register your models here.
#映射到admin后台管理系统
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name','status','create_time','id']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name','create_time','id']

admin.site.register(Project,ProjectAdmin)
admin.site.register(Module,ModuleAdmin)