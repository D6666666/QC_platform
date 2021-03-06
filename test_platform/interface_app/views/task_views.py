#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from interface_app.models import TestTask,TestResult
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#请求用例管理页面
@login_required
def task_manage(request):
    if request.method == 'GET':
        testtasks = TestTask.objects.get_queryset().order_by('id')
        paginator = Paginator(testtasks,10)
        page = request.GET.get("page")
        # form = ModuleForm()
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request,'task/task_manage.html',{'type':'list',"testtasks":contacts})
    else:
        return HttpResponse("404")

#搜索功能
@login_required
def search_task_name(request):
    if request.method == "GET":
        task_name = request.GET.get('task_name', "")
        tasks = TestTask.objects.filter(name__contains=task_name)
        paginator = Paginator(tasks, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)

        return render(request, "task/task_manage.html", {
            "type": "list",
            "testtasks": contacts,
            "task_name": task_name,
        })
    else:
        return HttpResponse("404")

#删除任务数据
@login_required
def delete_task(request,tid):
    TestTask.objects.get(id=tid).delete()
    return HttpResponseRedirect('/interface/task_manage/')

#新增任务
@login_required
def add_task(request):
    if request.method == 'GET':
        # form = TestCaseForm()
        return render(request,'task/add_task.html',{'type':'add'})
    else:
        return HttpResponse("404")

#编辑任务
@login_required
def edit_task(request,tid):
    if request.method == 'GET':
        # task_id = request.GET.get("task_id")
        return render(request,'task/edit_task.html',{'type':'edit'})
    else:
        return HttpResponse("404")

# 查看任务结果列表
@login_required
def task_result_list(request, tid):
    if request.method == "GET":
        task_obj = TestTask.objects.get(id=tid)
        result_list = TestResult.objects.filter(task_id=tid)

        return render(request, "task/result_task.html", {
            "type": "result",
            "task_name": task_obj.name,
            "task_result_list": result_list,
        })
    else:
        return HttpResponse("404")

