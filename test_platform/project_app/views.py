from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project,Module
from django.http import HttpResponseRedirect
from project_app.forms import ProjectForm

# Create your views here.

@login_required  #判断用户是否登陆
def project_manage(request):
    username = request.session.get('user','') #读取浏览器session
    projects = Project.objects.all()
    return render(request,'project_manage.html',{'user':username,'projects':projects,'type':'list'})

#新增项目处理：包含请求表单页面、提交表单数据
@login_required
def add_project(request):
    if request.method == 'POST':  #提交表单的post请求
        form = ProjectForm(request.POST)  #用ProjectForm校验表单数据
        if form.is_valid():  #判断表单数据校验结果
            #获取表单数据
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            #保存表单数据到库
            Project.objects.create(name=name,describe=describe)
            return HttpResponseRedirect('/manage/project_manage/')
    else:  #进入表单页面的get请求
        form = ProjectForm()
    return render(request,'project_manage.html',{'form':form,'type':'add'})


#修改项目数据
@login_required
def edit_project(request,pid):
    porject = Project.objects.get(id=pid)
    if request.method == 'POST':  #提交表单的post请求
        form = ProjectForm(request.POST)  #用ProjectForm校验表单数据
        # 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
        form = ProjectForm(instance=porject, data=request.POST)
        form.save()  # 保存
        if form.is_valid():  #判断表单数据校验结果
            return HttpResponseRedirect('/manage/project_manage/')
    else:  #进入表单页面的get请求
        if pid:
            form = ProjectForm(instance=porject)
    return render(request,'project_manage.html',{'form':form,'type':'edit'})

#删除项目数据
@login_required
def delete_project(request,pid):
    Project.objects.get(id=pid).delete()
    return HttpResponseRedirect('/manage/project_manage/')