from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth

# Create your views here.

#首页
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
                pass
            else:
                return render(request,'index.html',{'error':'用户名或者密码错误！'})


