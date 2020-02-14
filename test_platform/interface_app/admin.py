from django.contrib import admin
from interface_app.models import TestCase

# Register your models here.
#映射到admin后台管理系统
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['module','name','url','req_method','req_method','req_type','req_header','req_parameter','responses_assert']


admin.site.register(TestCase,TestCaseAdmin)

