#!/usr/bin/env python 
# coding:utf-8 
#author:cq
from django.contrib import admin
from django.urls import path,include
from interface_app import views

urlpatterns = [
    path('case_manage/', views.case_manage),
    path('api_debug/', views.api_debug),
    path('debug/', views.debug),
    path('save_case/', views.save_case),
    path('get_project_list/', views.get_project_list),
    path('delete_case/<int:cid>/', views.delete_case),
]