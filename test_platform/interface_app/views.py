import requests,json,validators
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from interface_app.forms import TestCaseForm
from project_app.models import Module,Project
from test_platform import common
from interface_app.models import TestCase
# Create your views here.

#请求用例管理页面
@login_required
def case_manage(request):
    testcases = TestCase.objects.all()
    if request.method == 'GET':
        return render(request,'case_manage.html',{'type':'list',"testcases":testcases})
    else:
        return HttpResponse("404")

#删除用例数据
@login_required
def delete_case(request,cid):
    TestCase.objects.get(id=cid).delete()
    return HttpResponseRedirect('/interface/case_manage/')

#新增&调试用例页面
@login_required
def debug(request):
    if request.method == 'GET':
        form = TestCaseForm()
        return render(request,'debug.html',{'form':form,'type':'debug'})
    else:
        return HttpResponse("404")


#接口调试
# @csrf_exempt
@login_required
def api_debug(request):
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
                                ,req_type=type_,req_header=header,req_parameter=parameter)
        if case is not None:
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