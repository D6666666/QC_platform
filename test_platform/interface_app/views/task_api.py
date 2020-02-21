#!/usr/bin/env python 
# coding:utf-8 
#author:cq
import requests,json,validators
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from project_app.models import Module,Project
from test_platform import common
from interface_app.models import TestCase,TestTask
from django.views.decorators.csrf import csrf_exempt


#获取接口用例列表
@csrf_exempt
@login_required
def get_case_list(request):
    #项目——》模块——》用例
    if request.method == "GET":
        cases_list = []
        projects = Project.objects.all()
        for project in projects:
            modules = Module.objects.filter(project_id = project.id)
            for module in modules:
                cases = TestCase.objects.filter(module_id = module.id)
                for case in cases:
                    case_info = project.name + "--->" + module.name + "--->" + case.name
                    case_dict = {
                        "id":case.id,
                        "name":case_info
                    }
                    cases_list.append(case_dict)
        return common.response_succeed(data=cases_list)
    else:
        return common.response_failed("请求方法错误！")

#保存任务
def save_task(request):
    if request.method == "POST":
        name = request.POST.get("task_name", "")
        describe = request.POST.get("task_describe", "")
        cases = request.POST.get("task_cases", "")
        if name == '':
            return common.response_failed("名称不能为空！")
        if cases == '':
            return common.response_failed("用例不能为空！")
        task = TestTask.objects.create(name = name,describe=describe,cases=cases,status=0)
        if task is not None:
            return common.response_succeed("保存成功！")

    else:
        return common.response_failed("请求方法错误！")