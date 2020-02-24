#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.contrib import admin
from django.urls import path,include
from interface_app.views import case_views,case_api,task_views,task_api

urlpatterns = [
    #用例管理
    #views
    path('case_manage/', case_views.case_manage),
    path('edit_case/<int:cid>/', case_views.edit_case),
    path('delete_case/<int:cid>/', case_views.delete_case),
    path('add_case/', case_views.add_case),
    path('search_case_name/', case_views.search_case_name),

    #api
    path('debug_case/', case_api.debug_case),
    path('save_case/', case_api.save_case),
    path('update_case/', case_api.update_case),
    path('get_project_list/', case_api.get_project_list),
    path('get_case_info/', case_api.get_case_info),
    path('api_assert/', case_api.api_assert),

    #任务管理
    #views
    path('task_manage/', task_views.task_manage),
    path('search_task_name/', task_views.search_task_name),
    path('add_task/', task_views.add_task),
    path('delete_task/<int:tid>/', task_views.delete_task),
    path('edit_task/<int:tid>/', task_views.edit_task),

    #api
    path('get_case_list/', task_api.get_case_list),
    path('save_task/', task_api.save_task),
    path('get_task_info/', task_api.get_task_info),
]