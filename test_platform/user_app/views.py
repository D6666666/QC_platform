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
        user = auth.authenticate(username=username,password=password)  #登陆验证
        if user is not None:
            pass


