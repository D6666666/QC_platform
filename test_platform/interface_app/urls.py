#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.contrib import admin
from django.urls import path,include
from interface_app.views import case_views,case_api

urlpatterns = [
    #api
    path('case_manage/', case_views.case_manage),
    path('edit_case/<int:cid>/', case_views.edit_case),
    path('delete_case/<int:cid>/', case_views.delete_case),
    path('add_case/', case_views.add_case),
    path('search_case_name/', case_views.search_case_name),

    #views
    path('debug_case/', case_api.debug_case),
    path('save_case/', case_api.save_case),
    path('update_case/', case_api.update_case),
    path('get_project_list/', case_api.get_project_list),
    path('get_case_info/', case_api.get_case_info),
    path('api_assert/', case_api.api_assert),
]