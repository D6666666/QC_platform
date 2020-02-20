import requests,json,validators
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from interface_app.forms import TestCaseForm
from project_app.models import Module,Project
from test_platform import common
from interface_app.models import TestCase
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from project_app.forms import ModuleForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#请求用例管理页面
@login_required
def case_manage(request):
    if request.method == 'GET':
        # testcases = TestCase.objects.all()
        testcases = TestCase.objects.get_queryset().order_by('id')
        paginator = Paginator(testcases,5)
        page = request.GET.get("page")
        form = ModuleForm()
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request,'case_manage.html',{'type':'list',"testcases":contacts,"form":form})
    else:
        return HttpResponse("404")


#搜索功能
@login_required
def search_case_name(request):
    if request.method == "GET":
        case_name = request.GET.get('case_name', "")
        cases = TestCase.objects.filter(name__contains=case_name)

        paginator = Paginator(cases, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)

        return render(request, "case_manage.html", {
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
        form = TestCaseForm()
        return render(request,'add_case.html',{'form':form,'type':'debug'})
    else:
        return HttpResponse("404")

#新增用例
@login_required
def add_case(request):
    if request.method == 'GET':
        form = TestCaseForm()
        return render(request,'add_case.html',{'form':form,'type':'add'})
    else:
        return HttpResponse("404")

#编辑用例
@login_required
def edit_case(request,cid):
    if request.method == 'GET':
        case_id = request.GET.get("case_id")
        return render(request,'edit_case.html',{'type':'edit'})
    else:
        return HttpResponse("404")

#接口调试
# @csrf_exempt
@login_required
def debug_case(request):
    if request.method == 'POST':
        url = request.POST.get("req_url",'')
        method = request.POST.get("req_method",'')
        type_ = request.POST.get("req_type",'')
        header = request.POST.get("req_header",'')
        parameter = request.POST.get("req_parameter",'')
        if validators.url(url) != True:
            return common.response_failed("请检查URL！")
        if method not in ['post','get']:
            return common.response_failed("请检查请求方法！")
        if header != '':
            try:
                header_dict = json.loads(header.replace("'", "\""))
                if type(header_dict) != dict:
                    raise TypeError
            except Exception:
                return common.response_failed("请检查header格式！")
        else:
            header_dict = None

        if parameter != '':
            try:
                payload = json.loads(parameter.replace("'", "\""))
                if type(payload) != dict:
                    raise TypeError
            except json.decoder.JSONDecodeError:
                return common.response_failed("请检查参数的格式！")
        else:
            payload = None

        if method == "get":
            if type_ == "from":
                r = requests.get(url, headers=header_dict, params=payload)
            else:
                return common.response_failed("参数类型错误")

        if method == "post":
            if type_ == "from":
                r = requests.post(url, headers=header_dict, data=payload)
            elif type_ == "json":
                r = requests.post(url, headers=header_dict, json=payload)
            else:
                return common.response_failed("参数类型错误")
        print(r.text)
        return common.response_succeed(data=r.text)
    else:
        return common.response_failed("请求方法错误")

#保存测试用例
@login_required
def save_case(request):
    if request.method == 'POST':
        name = request.POST.get("name", "")
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method", "")
        parameter = request.POST.get("req_parameter", "")
        type_ = request.POST.get("req_type", "")
        header = request.POST.get("header", "")
        module_name = request.POST.get("module", "")
        project_name = request.POST.get("project", "")
        assert_text = request.POST.get("assert_text", "")
        if validators.url(url) != True:
            return common.response_failed("请检查URL！")
        if method not in ['post','get']:
            return common.response_failed("请检查请求方法！")
        if header != '':
            try:
                header_dict = json.loads(header.replace("'", "\""))
                if type(header_dict) != dict:
                    raise TypeError
            except Exception:
                return common.response_failed("请检查header格式！")
        else:
            header = "{}"

        if parameter != '':
            try:
                payload = json.loads(parameter.replace("'", "\""))
                if type(payload) != dict:
                    raise TypeError
            except json.decoder.JSONDecodeError:
                return common.response_failed("请检查参数的格式！")
        else:
            parameter = "{}"

        project = Project.objects.get(name = project_name)
        module_obj = Module.objects.get(name = module_name,project__id=project.id)
        case = TestCase.objects.create(name = name,module=module_obj,url=url,req_method=method
                                ,req_type=type_,req_header=header,req_parameter=parameter,responses_assert=assert_text)
        if case is not None:
            return common.response_succeed("保存成功！")

    else:
        return HttpResponse("404")


#更新测试用例
@login_required
def update_case(request):
    if request.method == 'POST':
        case_id = request.POST.get("cid", "")
        name = request.POST.get("name", "")
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method", "")
        parameter = request.POST.get("req_parameter", "")
        type_ = request.POST.get("req_type", "")
        header = request.POST.get("header", "")
        module_name = request.POST.get("module", "")
        project_name = request.POST.get("project", "")
        assert_text = request.POST.get("assert_text", "")
        if validators.url(url) != True:
            return common.response_failed("请检查URL！")
        if method not in ['post','get']:
            return common.response_failed("请检查请求方法！")
        if header != '':
            try:
                header_dict = json.loads(header.replace("'", "\""))
                if type(header_dict) != dict:
                    raise TypeError
            except Exception:
                return common.response_failed("请检查header格式！")
        else:
            header = "{}"

        if parameter != '':
            try:
                payload = json.loads(parameter.replace("'", "\""))
                if type(payload) != dict:
                    raise TypeError
            except json.decoder.JSONDecodeError:
                return common.response_failed("请检查参数的格式！")
        else:
            parameter = "{}"

        project = Project.objects.get(name = project_name)
        module_obj = Module.objects.get(name = module_name,project__id=project.id)
        try:
            TestCase.objects.filter(id=case_id).update(name = name,module=module_obj,url=url,req_method=method
                                ,req_type=type_,req_header=header,req_parameter=parameter,responses_assert=assert_text)
        except Exception as e:
            return common.response_failed("保存失败！")
        return common.response_succeed("保存成功！")
    else:
        return HttpResponse("404")

#获取项目模块列表
@login_required
def get_project_list(request):
    '''
        返回一个列表
                [{name: '项目AAAA',moduleList: ["模块a", "模块b", "模块c"]},
                {name: '项目BBB',moduleList: ["模块1", "模块2", "模块3"]}]
    '''
    project_list = Project.objects.all()
    datalist = []
    for project in project_list:
        project_dict = {"name":project.name}
        moduleList = Module.objects.filter(project_id=project.id)
        if len(moduleList) != 0:
            module_name = []
            for module in moduleList:
                module_name.append(module.name)
            project_dict['moduleList'] = module_name
            datalist.append(project_dict)
    return JsonResponse({"success":"true","data":datalist})

#获取接口用例信息
@csrf_exempt
@login_required
def get_case_info(request):
    if request.method == "POST":
        case_id = request.POST.get('caseId','')
        if case_id == '':
            return JsonResponse({"success":"false","message":"case id Null."})
        case_obj = TestCase.objects.get(pk=case_id)
        module_obj = Module.objects.get(pk=case_obj.module_id)
        project_obj = Project.objects.get(pk=module_obj.project_id)


        case_info = {
            "project_name":project_obj.name,
            "module_name":module_obj.name,
            "name" : case_obj.name,
            "url" : case_obj.url,
            "req_method": case_obj.req_method,
            "req_type": case_obj.req_type,
            "req_header": case_obj.req_header,
            "req_parameter": case_obj.req_parameter,
            "responses_assert": case_obj.responses_assert,
        }
        return JsonResponse({"success": "true", "message": "ok","data":case_info})
    else:
        return HttpResponse("404")


#验证预期结果
@login_required
def api_assert(request):
    if request.method =="POST":
        result_test = request.POST.get("result","")
        assert_test = request.POST.get("assert", "")
        if result_test == '' or assert_test == '':
            return JsonResponse({"success":"false","message":"验证数据或者验证结果不能为空！"})
        try:
            assert assert_test in result_test
        except AssertionError:
            return JsonResponse({"success": "false", "message": "验证失败！"})
        else:
            return JsonResponse({"success": "false", "message": "验证成功！"})
    else:
        return HttpResponse("404")
