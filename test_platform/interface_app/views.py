import requests,json,validators
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from test_platform import common
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
def debug(request):
    if request.method == 'GET':
        return render(request,'debug.html',{'type':'debug'})
    else:
        return HttpResponse("404")


#接口调试
@csrf_exempt
@login_required
def api_debug(request):
    if request.method == 'POST':
        url = request.POST.get("req_url")
        method = request.POST.get("req_method")
        type_ = request.POST.get("req_type")
        header = request.POST.get("req_header")
        parameter = request.POST.get("req_parameter")
        if validators.url(url) != True:
            return common.response_failed("请检查URL！")
        if method not in ['post','get']:
            return common.response_failed("请检查请求方法！")
        print(header)
        print(type(header))
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
