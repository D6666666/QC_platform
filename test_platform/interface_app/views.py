from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

#请求用例管理页面
@login_required
def case_manage(request):
    if request.method == 'GET':
        return render(request,'case_manage.html',{'type':'list'})
    else:
        return HttpResponse("404")

#新增&调试用例页面
@login_required
def api_debug(request):
    if request.method == 'GET':
        return render(request,'api_debug.html',{'type':'debug'})
    else:
        return HttpResponse("404")