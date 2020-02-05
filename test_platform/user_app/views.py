from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth

# Create your views here.

#首页from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'index.html')


#处理登陆请求
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return render(request,'index.html',{'error':'用户名或者密码不能为空！'})
        else:
            user = auth.authenticate(username=username,password=password)  #登陆验证
            if user is not None:
                auth.login(request,user) #记录登陆状态
                request.session['user'] = username
                return HttpResponseRedirect("/project_manage/")
            else:
                return render(request,'index.html',{'error':'用户名或者密码错误！'})


#退出登陆
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return  response



