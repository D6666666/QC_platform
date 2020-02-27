#!/usr/bin/env python 
# coding:utf-8 
#author:cq
import requests,json,validators,os,time
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from project_app.models import Module,Project
from test_platform import common
from interface_app.extend.task_thread import TaskThread
from interface_app.models import TestCase,TestTask,TestResult
from django.views.decorators.csrf import csrf_exempt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
task_file = os.path.join(BASE_DIR,"interface_app","extend")
resource = os.path.join(BASE_DIR,"resource")

#获取接口用例列表
@csrf_exempt
@login_required
def get_case_list(request):
    #项目——》模块——》用例
    if request.method == "GET":
        task_cases = request.GET.get("task_case", "")
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
        data = {"cases_list":cases_list,"check_cases":task_cases}
        return common.response_succeed(data=data)
    else:
        return common.response_failed("请求方法错误！")

#保存任务
@login_required
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

#获取任务
@csrf_exempt
@login_required
def get_task_info(request):
    if request.method == "POST":
        task_id = request.POST.get('taskId','')
        if task_id == '':
            return common.response_failed("task id Null.")
        task_obj = TestTask.objects.get(pk=task_id)
        task_info = {
            "task_name":task_obj.name,
            "task_describe":task_obj.describe,
            "task_cases" : task_obj.cases,
        }
        return common.response_succeed(data=task_info)
    else:
        return HttpResponse("404")

#运行任务
@csrf_exempt
@login_required
def run_task(request):
    if request.method == "POST":
        tid = request.POST.get("task_id", "")
        if tid == "":
            return common.response_failed("任务ID不能为空")

        task_list = TestTask.objects.all()
        runing_task = 0
        for task in task_list:
            if task.status == 1:
                runing_task = 1
                break
        if runing_task == 1:
            return common.response_failed("当前有任务正在执行...")
        else:
            TaskThread(tid).new_run()
            return common.response_succeed(message="已执行")
    else:
        return common.response_failed("请求方法错误")

# 查看任务结果
@csrf_exempt
@login_required
def task_result(request):
    if request.method == "POST":
        rid = request.POST.get("result_id", "")
        result_obj = TestResult.objects.get(id=rid)
        data = {
            "result": result_obj.result,
        }
        return common.response_succeed(message="获取成功！", data=data)
    else:
        return common.response_failed("请求方法错误")