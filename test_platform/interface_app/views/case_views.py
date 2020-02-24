import requests,json,validators
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from interface_app.models import TestCase
from project_app.forms import ModuleForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

#请求用例管理页面
@login_required
def case_manage(request):
    if request.method == 'GET':
        # testcases = TestCase.objects.all()
        testcases = TestCase.objects.get_queryset().order_by('id')
        paginator = Paginator(testcases,10)
        page = request.GET.get("page")
        # form = ModuleForm()
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request,'case/case_manage.html',{'type':'list',"testcases":contacts})
    else:
        return HttpResponse("404")

#搜索功能
@login_required
def search_case_name(request):
    if request.method == "GET":
        case_name = request.GET.get('case_name', "")
        cases = TestCase.objects.filter(name__contains=case_name)

        paginator = Paginator(cases, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)

        return render(request, "case/case_manage.html", {
            "type": "list",
            "testcases": contacts,
            "case_name": case_name,
        })
    else:
        return HttpResponse("404")



# def search_case_name(request):
#     if request.method == 'GET':
#         form_p = ModuleForm(request.POST)
#         if form_p.is_valid():  #判断表单数据校验结果
#             #获取表单数据
#             project = form_p.cleaned_data['project']
#             project_id = Project.objects.get(name=project).id
#             module_id = Module.objects.filter(project_id=project_id)
#             module = []
#             for i in module_id: module.append(i.id)
#             name = request.GET.get("case_name")
#             testcases = TestCase.objects.filter(name__contains=name, module_id__in=module)
#         else:
#             project_id = ""
#             module_id = ['']
#             name = request.GET.get("case_name")
#             testcases = TestCase.objects.filter(name__contains=name)
#         paginator = Paginator(testcases, 2)
#         page = request.GET.get("page")
#         form = ModuleForm(instance=module_id[0])
#         try:
#             contacts = paginator.page(page)
#         except PageNotAnInteger:
#             contacts = paginator.page(1)
#         except EmptyPage:
#             contacts = paginator.page(paginator.num_pages)
#         return render(request,'case_manage.html',{'type':'list',"testcases":contacts,'case_name':name})
#     else:
#         return HttpResponse("404")


#删除用例数据
@login_required
def delete_case(request,cid):
    TestCase.objects.get(id=cid).delete()
    return HttpResponseRedirect('/interface/case_manage/')

#新增&调试用例页面
@login_required
def add_case(request):
    if request.method == 'GET':
        # form = TestCaseForm()
        return render(request,'case/add_case.html',{'type':'add'})
    else:
        return HttpResponse("404")



#编辑用例
@login_required
def edit_case(request,cid):
    if request.method == 'GET':
        # case_id = request.GET.get("case_id")
        return render(request,'case/edit_case.html',{'type':'edit'})
    else:
        return HttpResponse("404")


