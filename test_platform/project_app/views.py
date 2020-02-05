from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project,Module

# Create your views here.


@login_required  #判断用户是否登陆
def project_manage(request):
    username = request.session.get('user','') #读取浏览器session
    projects = Project.objects.all()
    return render(request,'project_manage.html',{'user':username,'projects':projects,'type':'list'})

@login_required
def add_project(request):
    username = request.session.get('user','') #读取浏览器session
    projects = Project.objects.all()
    return render(request,'project_manage.html',{'user':username,'projects':projects,'type':'add'})