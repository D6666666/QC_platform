from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project,Module
from django.http import HttpResponseRedirect
from project_app.forms import ModuleForm

# Create your views here.
#进入项目列表
@login_required  #判断用户是否登陆
def module_manage(request):
    username = request.session.get('user','') #读取浏览器session
    modules = Module.objects.all()
    return render(request,'module_manage.html',{
        'user':username,'modules':modules,'type':'list'})

#新增项目处理：包含请求表单页面、提交表单数据
@login_required
def add_module(request):
    if request.method == 'POST':  #提交表单的post请求
        form = ModuleForm(request.POST)  #用ProjectForm校验表单数据
        if form.is_valid():  #判断表单数据校验结果
            #获取表单数据
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            #保存表单数据到库
            Module.objects.create(name=name,describe=describe,project=project)
            return HttpResponseRedirect('/manage/module_manage/')
    else:  #进入表单页面的get请求
        form = ModuleForm()
    return render(request,'module_manage.html',{'form':form,'type':'add'})


#修改项目数据
@login_required
def edit_module(request,mid):
    module = Module.objects.get(id=mid)
    if request.method == 'POST':  #提交表单的post请求
        # form = ModuleForm(request.POST)  #用ProjectForm校验表单数据
        # 如果是post,instance=article当前数据填充表单，并用data=request.POST获取到表单里的内容
        form = ModuleForm(instance=module, data=request.POST)
        form.save()  # 保存
        if form.is_valid():  #判断表单数据校验结果
            return HttpResponseRedirect('/manage/module_manage/')
    else:  #进入表单页面的get请求
        if mid:
            form = ModuleForm(instance=module)
    return render(request,'module_manage.html',{'form':form,'type':'edit'})

#删除项目数据
@login_required
def delete_module(request,mid):
    Module.objects.get(id=mid).delete()
    return HttpResponseRedirect('/manage/module_manage/')